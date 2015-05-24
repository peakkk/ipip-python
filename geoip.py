#!/usr/bin/env python
# coding: utf-8

'''全球 IPv4 地址归属地数据库(ipip.net 版)

高春辉(pAUL gAO) <gaochunhui@gmail.com>
Build 20141009 版权所有 ipip.net
(C) 2006 - 2014 保留所有权利
请注意及时更新 IP 数据库版本
数据问题请加 QQ 群: 346280296
'''

__author__ = 'Peakkk'

from os import path
import socket
import struct



_IP_DATA = path.dirname( path.realpath(__file__) )+ '/17monipdb.dat'

class GeoIP:
    def __init__(self):
        try:
            self.data_file = open(_IP_DATA, 'rb')
        except Exception:
            raise Exception("Could not open data file")

        self.offset, = struct.unpack('>I', self.data_file.read(4))
        if self.offset < 4:
            raise Exception("Invalid data file")

        self.index = self.data_file.read( self.offset - 4 )


    def find(self, host):
        try:
            ip = socket.gethostbyname(host)
        except Exception as e:
            raise e

        ip_segs = ip.split('.')
        ipn = socket.inet_aton(ip)
        
        offset = int( ip_segs[0] ) * 4
        start, = struct.unpack("<I", self.index[offset:offset+4])

        max_comp_len = self.offset - 1024 - 4
        index_offset = index_len = None
        for i in xrange(start * 8 + 1024, max_comp_len, 8):
            if self.index[i : i+4] >= ipn:
                index_offset, = struct.unpack('<I', self.index[i+4: i+7] + '\x00')
                index_len, = struct.unpack('B', self.index[i+7])

                break

        if index_offset is None:
            raise Exception('No such data')

        self.data_file.seek(self.offset + index_offset - 1024)
        
        raw_string = self.data_file.read( index_len )
        raw_string = raw_string.decode('utf-8', 'ignore')

        return raw_string.split('\t')



_geo_ip = GeoIP()

def find(host):
    ''' 查找对应IP/主机名/域名的地理位置信息
    
    find("www.baidu.com")
        -> [u'\u4e2d\u56fd', u'\u6d59\u6c5f', u'\u676d\u5dde', u'']

    find("114.114.114.114")
        -> [u'114DNS', u'114DNS', u'', u'']

    如果没有对应信息，则抛出异常
    '''
    return _geo_ip.find(host)
    

if __name__ == '__main__':
    print find("114.114.114.114")
    print find("www.baidu.com")

