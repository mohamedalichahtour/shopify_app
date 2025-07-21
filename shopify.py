import os
import requests

SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

def get_fulfillments(order_id):
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2023-04/graphql.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    }
    query = """
    query getOrderFulfillments($id: ID!) {
      order(id: $id) {
        fulfillments {
          id
          status
          trackingInfo {
            number
            company
            url
          }
        }
      }
    }
    """
    variables = {"id": order_id}
    response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
    return response.json()
