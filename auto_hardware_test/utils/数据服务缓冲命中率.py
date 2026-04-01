#数据服务缓存命中率=(数据服务日志中平均带宽-zabbix中数据盘平均带宽)/数据服务日志中平均带宽

def database_bw(path):

    global file_path2, file_path1
    import re
    #
    # file_path1=r'../log/dataservice_20210406.log'
    # file_path2=r'../log/diskservice_20210406.log'

    # path=r'../log/data_disk/1'

    import os
    for (root,dirs,files) in os.walk(path):
        for file in files:
            if "dataservice" in os.path.join(root,file):
                file_path1=os.path.join(root,file)
            else:
                file_path2=os.path.join(root,file)


    temp_list1 = []
    temp_list2 = []
    with open(file_path2,'r',encoding='utf-8') as f1:

        contents1=f1.read().splitlines()

        for content1 in contents1:
            try:
                  # *[15:39:38.468][9e85][Info][dispatcher/dispatcher.cpp:420][on_query_service_cache_hit_rate]|requests: 9380898, hits: 7546906, image_hit_rate:80.4*

                temp1 = re.match(r'.*?hits:(.*?)image_hit_rate:(.*)',content1)

                  # (.*)第二个匹配分组，.*代表匹配除换行符之外的所有字符。
                  # (.* ?)第一个匹配分组，.* ? 后面多个问号，代表非贪婪模式，也就是说只匹配符合条件的最少字符
                  # 后面的一个. * 没有括号包围，所以不是分组，匹配效果和第一个一样，但是不计入匹配结果中。


                key_word=temp1.group(2)

                if key_word is None:  # 进一步确定错误类型

                    pass   #让输出空的内容不展示，不占空格

                # print(key_word

                # print(type(key_word))

                temp_list2.append(key_word)

            except AttributeError:

                pass
    # print(len(temp_list2))
    # print(temp_list2)
    print("镜像缓存命中率为：",temp_list2[-1])

    with open(file_path1,'r') as f:

        contents=f.read().splitlines()  #是一个列表

        for content in contents:

            try:

                temp = re.match(r'.*?speed:(.*?)MB/s',content)

                key_word=temp.group(1)

                if key_word is None:  # 进一步确定错误类型

                    pass   #让输出空的内容不展示，不占空格

                # print(key_word

                # print(type(key_word))

                temp_list1.append(key_word)

            except AttributeError:

                pass
            # except Exception as result:

            #     print("出错原因：", result)

    # print(temp_list)

    sum=0

    for item in temp_list1:

        sum+=float(item)

    Avenage=sum/float(len(temp_list1))

    print('数据服务日志中平均带宽：',Avenage,'MB/s')

    return Avenage

if __name__ == '__main__':

    path=input("输入需要查询结果的路径：")
    data_avg=database_bw(path=path)

    zabbix_bw=float(input('输入zabbix中的数据盘的平均带宽(MB/s)：'))

    Data_service_cache_hit_rate=(data_avg-zabbix_bw)/data_avg

    print('数据服务缓存命中率为：',Data_service_cache_hit_rate)


    # x='123'
    #
    # if x.__eq__('123'):
    #
    #     print('sucess')

