from config import mydb

mycol = mydb["tmp_teacher"]
x = mycol.delete_many({})
print(x.deleted_count, " documents deleted.")

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
# print(x.deleted_count, " documents deleted.")
#
# mycol = mydb["student"]
# x = mycol.delete_many({})
# print(x.deleted_count, " documents deleted.")
#
#
# mycol = mydb["tree"]
# x = mycol.delete_many({})
# print(x.deleted_count, " documents deleted.")

# mycol = mydb["tmp_student"]
# x = mycol.delete_many({})
# print(x.deleted_count, " documents deleted.")
# # #
# mycol = mydb["tmp"]
# x = mycol.delete_many({})
# print(x.deleted_count, " documents deleted.")
# #
# mycol = mydb["alerts"]
# x = mycol.delete_many({})
# print(x.deleted_count, " documents deleted.")
# #
