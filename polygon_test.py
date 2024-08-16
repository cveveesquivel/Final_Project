from polygon import RESTClient
client = RESTClient(api_key = "EmMATDGzKUU0Lq96vumklRHczv17FHBb")

s1 = 'AAPL'
s2 = 'ZZDJ'



aggs = client.get_previous_close_agg(s1)
bad = client.get_previous_close_agg(s2)
print(type(aggs))
print(aggs)
print(type(bad))