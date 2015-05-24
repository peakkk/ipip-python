# ipip-python

## 说明
此项目是 ipip.net 离线数据库的python版本
最新数据库下载地址:
    [http://www.ipip.net/download.html](http://www.ipip.net/download.html)

## 用法
```python
import geoip

# 返回 [u'114DNS', u'114DNS', u'', u'']
geoip.find('114.114.114.114')


# 返回 [u'\u4e2d\u56fd', u'\u6d59\u6c5f', u'\u676d\u5dde', u'']
geoip.find('www.baidu.com')
```



