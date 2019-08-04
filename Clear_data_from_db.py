import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
# mycol = mydb["student"]
# x = mycol.delete_many({})
# print(x.deleted_count, " documents deleted.")

mycol = mydb["tmp_pie"]
x = mycol.delete_many({})
print(x.deleted_count, " documents deleted.")

mycol = mydb["tmp_column"]
x = mycol.delete_many({})
print(x.deleted_count, " documents deleted.")

mycol = mydb["tmp"]
x = mycol.delete_many({})
print(x.deleted_count, " documents deleted.")
# #
# mycol = mydb["school"]
# x = mycol.delete_many({})
# print(x.deleted_count, " documents deleted.")
#
# mycol = mydb["region"]
# x = mycol.delete_many({})
# print(x.deleted_count, " documents deleted.")
#
# mycol = mydb["subject"]
# x = mycol.delete_many({})
# print(x.deleted_count, " documents deleted.")
#
# mycol = mydb["teacher"]
# x = mycol.delete_many({})
#
# print(x.deleted_count, " documents deleted.")
# #
# mycol = mydb["tree"]
# x = mycol.delete_many({})
# print(x.deleted_count, " documents deleted.")
