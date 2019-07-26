# -*- coding:utf-8 -*-
"""
    version: 
    author : wkh
    time   : 2019/7/26 16:08
    file   : AliPay.py
    
"""
from alipay import AliPay

alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAz6mmwgohEIq7gpO/acdRire4AXe6GeohT13mRLWIYK+Gf/ezxT+GjG1DM6UJX+JKn1eUacpKBCMe83GxcTFXIdr4Np136TDJ7OcAbprs4csmUa/vw2bxQXBK6PYrYwblUAxN0HlpJh7kPwM7IKut9e/XDMorGLqTgBOI/dLCvfIdNU1jZ+ozppIo93fEGqTjC/HUis5EziyEHmZbnLJGGgufdiVA2H+HVL68sDUd1VpSWqHAE+HrH3sVwP80wR2zgcz47XYUK5/0h0m7QcW4jbqNEvMJ+CRHS7YLC/ucBwZrNGCyXTEXRx0h4mrz4FeAKyFPX0zy0ZY+pBRdTgOltQIDAQAB
-----END PUBLIC KEY-----"""

alipay_private_key_string = """-----BEGIN REA PRIVATE KEY-----
MIIEowIBAAKCAQEAz6mmwgohEIq7gpO/acdRire4AXe6GeohT13mRLWIYK+Gf/ezxT+GjG1DM6UJX+JKn1eUacpKBCMe83GxcTFXIdr4Np136TDJ7OcAbprs4csmUa/vw2bxQXBK6PYrYwblUAxN0HlpJh7kPwM7IKut9e/XDMorGLqTgBOI/dLCvfIdNU1jZ+ozppIo93fEGqTjC/HUis5EziyEHmZbnLJGGgufdiVA2H+HVL68sDUd1VpSWqHAE+HrH3sVwP80wR2zgcz47XYUK5/0h0m7QcW4jbqNEvMJ+CRHS7YLC/ucBwZrNGCyXTEXRx0h4mrz4FeAKyFPX0zy0ZY+pBRdTgOltQIDAQABAoIBAFqroYMhtxQo7vxxlGcUPzdJRk9lvl0oTEkCH9OqS5Sjrx9awSSDuzS/VFNNYQ17mcd/Du8uAylRSGdVIfvhZkEDAdOe58dqpRAKQLcKcBmagO2z2wU/gmFnLV4Qdhsz3JYZ+TPofw/E9zXILF30d+1lPkl4UF7owBRw8ySYjK0wKyiK/2YqGFxQOLdvbzqYzt14kHW7u67g+NeV5/zcHCze9yXVymVAgUGctE/Fjm1vdJf+dOWr5qa3SPkGzd8a95rnW2pDkOc51ck7Q+9uq+xSRNyJAsL4u66ENagwYPaIdMdGtQ/FfERcUQcL32n+zAf5zVcA/aH6qGWoFV+PAFUCgYEA8Hbc4FB4OmmXTD0j1/aktIfqGJosGg8SWZZYfUNjRD0aorm2Z+kBKkHbwEpEGoIDF12aY2PLr01PDu/ZtA8b4A0d4wlH2vtFkJ2bWHDXLXxSDUFMM0w+RXlc4qlctAp4ikbh6oOgvWXybTqJ6LRglm0oGh3Ng5xBuPZYgC/EW7MCgYEA3RRE+siPjfMoiHlgPFFOAsiQfR/8HCP8Aq3tJYc2JSE3/EE3Iumd4s/TO2l+jTBhIj9pB8koBmxxiug65z+Mg9fj8lnQ/e4ZRQeGmZ2C/Kjy5dYEyBbNkZr0EkHgciMQhP0H3Ne5l+yGAjw/ENO3O479GxbpATH7S/sUah2uJPcCgYBfvSNx1/gWYaYQf6M+v/+RtS96Ph/i/C81JgvzS5pBOAbb1Q8PzhBdr7z7kVYOK8dpTSZD/h7BnAknDE3kR8O0b+R/WVmXkUWAL5ADJWI2xPGyP1ZEck20wX4+7GlxcV3OyCv4gBHGdsmPvafc07xFCA7YXxdNGDB+oO5ZkysdywKBgQDK/qGX5DBsFqlRJqHGwKDwzVhei8/hxujPTQRDQTPmQ+o0JW2LERd3+3vpQaSB37pQyAiYrYui2lAnS7VKQH+1T7ZuASp0/vsU9yQQSSDM/hSKFUmur8FxwOX7HaIJK0kv02Y00aAIb5Vc2BTQTpYgidq91Pt9rXcg/RpxlW8hYQKBgAEdfsZdixuI6eXP2nNKcuhSawphWeq8k2uwcdv+owLHD2LoQLW3RC6kJtxhzQNvnGpXUb6Sui/QJjp3vJieEoedUQ8Kc5dne6oDKaRIQHu5VbyIzvqrgncTvYg92PpYXT688ERCyppHaDFlAYKjTIHLhsxcynxhR4hba/UcHHyN
-----END REA PRIVATE KEY-----"""


alipay = AliPay(
    appid='2016101000652497',
    app_notify_url=None,
    app_private_key_string=alipay_private_key_string,
    alipay_public_key_string=alipay_public_key_string,
    sign_type='RSA2'
)

# 发起支付请求
order_str = alipay.api_alipay_trade_page_pay(
    out_trade_no='33334',  # 订单号
    total_amount=str(1100000.01),  # 支付金额
    subject='生鲜交易',  # 交易主题
    return_url=None,
    notify_url=None
)

print("https://openapi.alipaydev.com/gateway.do?"+order_str)