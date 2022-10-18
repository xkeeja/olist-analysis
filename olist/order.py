from antigravity import geohash
import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Order in the variable self, as well as all its attributes
        if is_delivered == True:
            orders_delivered = self.data['orders'].query("order_status == 'delivered'").copy()
        else:
            orders_delivered = self.data['orders'].copy()

        #datetime conversion
        orders_delivered['order_purchase_timestamp'] = pd.to_datetime(orders_delivered['order_purchase_timestamp'])
        orders_delivered['order_delivered_customer_date'] =  pd.to_datetime(orders_delivered['order_delivered_customer_date'])
        orders_delivered['order_estimated_delivery_date'] = pd.to_datetime(orders_delivered['order_estimated_delivery_date'])

        #new column calculations
        orders_delivered['wait_time'] = (orders_delivered['order_delivered_customer_date'] - orders_delivered['order_purchase_timestamp']).dt.days + ((orders_delivered['order_delivered_customer_date'] - orders_delivered['order_purchase_timestamp']).dt.seconds/86_400)

        orders_delivered['expected_wait_time'] = (orders_delivered['order_estimated_delivery_date'] - orders_delivered['order_purchase_timestamp']).dt.days + ((orders_delivered['order_estimated_delivery_date'] - orders_delivered['order_purchase_timestamp']).dt.seconds/86_400)

        orders_delivered['delay_vs_expected'] = (orders_delivered['order_delivered_customer_date'] - orders_delivered['order_estimated_delivery_date']).dt.days + ((orders_delivered['order_delivered_customer_date'] - orders_delivered['order_estimated_delivery_date']).dt.seconds/86_400)
        orders_delivered.loc[orders_delivered['delay_vs_expected'] < 0, 'delay_vs_expected'] = 0

        #final df filtering
        orders_delivered = orders_delivered[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']]

        return orders_delivered

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        orders_reviews = self.data['orders'].merge(self.data['order_reviews'], on='order_id')

        #define rating mapping function
        def key(row, rating):
            if row['review_score'] == rating:
                return 1
            return 0

        #new column calculations
        orders_reviews['dim_is_five_star'] = orders_reviews.apply(lambda row: key(row, 5), axis=1)
        orders_reviews['dim_is_one_star'] = orders_reviews.apply(lambda row: key(row, 1), axis=1)

        #final df filtering
        orders_reviews = orders_reviews[['order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score']]

        return orders_reviews

    def get_number_products(self):
        """
        Returns a DataFrame with:
        order_id, number_of_products
        """
        order_items = self.data['order_items'].copy()

        #calculate number of products and rename column
        order_items = order_items[['order_id','product_id']].groupby('order_id').count()
        order_items.rename(columns={'product_id': 'number_of_products'}, inplace=True)

        #reset index
        order_items.reset_index(inplace=True)

        return order_items

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        order_sellers = self.data['order_items'].copy()

        #calculate number of unique sellers and rename column
        order_sellers = order_sellers[['order_id','seller_id']].groupby('order_id').nunique()
        order_sellers.rename(columns={'seller_id': 'number_of_sellers'}, inplace=True)

        #reset index
        order_sellers.reset_index(inplace=True)

        return order_sellers

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        orders_price_freight = self.data['order_items'].copy()

        #aggregate price and freight value
        orders_price_freight = orders_price_freight.groupby('order_id').agg({'price': 'sum', 'freight_value': 'sum'})

        #reset index
        orders_price_freight.reset_index(inplace=True)

        return orders_price_freight

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        #starting df setup and cleanup
        geo = self.data['geolocation'].copy()
        orders = self.data['orders'].copy()
        customers = self.data['customers'].copy()
        items = self.data['order_items'].copy()
        sellers = self.data['sellers'].copy()

        geo.drop_duplicates(subset='geolocation_zip_code_prefix', inplace=True)
        location = orders.merge(customers, on='customer_id').merge(items, on='order_id').merge(sellers, on='seller_id')
        location_fil = location.filter(['order_id', 'customer_zip_code_prefix', 'seller_zip_code_prefix'])

        #customer lat lng
        location_fil = location_fil.merge(geo, left_on=['customer_zip_code_prefix'], right_on=['geolocation_zip_code_prefix'])
        location_fil.drop(columns=['geolocation_zip_code_prefix', 'geolocation_city','geolocation_state'], inplace=True)
        location_fil.rename(columns={'geolocation_lat': 'customer_lat', 'geolocation_lng': 'customer_lng'}, inplace=True)
        location_fil.drop_duplicates(inplace=True)

        #seller lat lng
        location_fil = location_fil.merge(geo, left_on=['seller_zip_code_prefix'], right_on=['geolocation_zip_code_prefix'])
        location_fil.drop(columns=['geolocation_zip_code_prefix', 'geolocation_city','geolocation_state'], inplace=True)
        location_fil.rename(columns={'geolocation_lat': 'seller_lat', 'geolocation_lng': 'seller_lng'}, inplace=True)
        location_fil.drop_duplicates(inplace=True)

        #remove duplicates
        location_fil.drop_duplicates(subset=['order_id'], inplace=True)

        #calculate distance
        location_fil['distance_seller_customer'] = location_fil.apply(lambda row: haversine_distance(row['customer_lng'], row['customer_lat'], row['seller_lng'], row['seller_lat']), axis=1)

        #final df filter
        location_fil = location_fil.filter(['order_id', 'distance_seller_customer'])

        return location_fil

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_products', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        all_data = self.get_wait_time(is_delivered).merge(self.get_review_score(), on='order_id').merge(self.get_number_products(), on='order_id').merge(self.get_number_sellers(), on='order_id').merge(self.get_price_and_freight(), on='order_id')

        if with_distance_seller_customer == True:
            all_data = all_data.merge(self.get_distance_seller_customer(), on='order_id')

        all_data.dropna(inplace=True)

        return all_data
