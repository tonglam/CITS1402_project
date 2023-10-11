# 1402-sqlite-project 测试食用方法

# Step 1 - Replace Files

将 `/sql` 文件夹下的`.sql`文件替换成自己的。

# Step 2 - Create Database

执行`main.py`中的`create_database()`函数，这一步会执行所有创建DDL语句，并检查基本的表结构、约束、索引是否正确。
同时，会生成trigger_monitor表，监控trigger的执行状态；建立另一个trigger:trigger_monitor，监控project的trigger的执行状态。

__Checklist__：

1. 成功执行所有`.sql`文件无报错。
2. 创建四个表：Phone, PhoneModel, rentalContract, Customer。
3. 检查基本表结构
    - Phone表
        - 三个字段：IMEI(TEXT), modelNumber(TEXT), modelName(TEXT)。
        - 主键：IMEI。
        - 外键：Phone.(modelNumber + modelName) -> PhoneModel.(modelNumber + modelName)。
    - PhoneModel表
        - 六个字段：modelNumber(TEXT), modelName(TEXT), storage(INTEGER), colour(TEXT), baseCost(REAL), dailyCost(REAL)。
        - 主键：modelNumber。
    - rentalContract表
        - 五个字段：customerId(INTEGER), IMEI(TEXT), dateOut(TEXT), dateBack(TEXT), rentalCost(Real)。
        - 主键：customerId + IMEI + dateOut。
        - 外键：rentalContract.customerID -> Customer.customerID, rentalContract.IMEI -> Phone.IMEI。
    - Customer表
        - 三个字段：customerId(INTEGER), customerName(TEXT), customerEmail(TEXT)。
        - 主键：customerId。

# Step 3 - Fake Data

执行`main.py`中的`fake_data()`函数,这一步会生成数据，插入上一步创建的四张表中，接下来会再次验证表约束。

__Checklist__：

1. 检查Primary Key
    - 随机从Phone表取一条数据，重新插入Phone表，检查是否报错。
    - 随机从PhoneModel表取一条数据，重新插入PhoneModel表，检查是否报错。
    - 随机从rentalContract表取一条数据，重新插入rentalContract表，检查是否报错。
    - 随机从Customer表取一条数据，重新插入Customer表，检查是否报错。
2. 检查Foreign Key
    - 随机从Phone表取一条数据，将其modelNumber修改为PhoneModel表不存在的值，检查是否报错。
    - 随机从Phone表取一条数据，将其modelName修改为PhoneModel表不存在的值，检查是否报错。
    - 随机从rentalContract表取一条数据，将其customerId修改为Customer表不存在的值，检查是否报错。
    - 随机从rentalContract表取一条数据，将其IMEI修改为Phone表不存在的值，检查是否报错。
3. 检查Check约束
    - 随机从Phone表取一条数据，将其IMEI截取前7位，检查是否报错。
    - 随机从Phone表取一条数据，将其IMEI截取前7位改为随机字母，检查是否报错。
    - 随机从Phone表取一条数据，将其IMEI加1，检查是否报错。

# Step 4 - Trigger

执行`main.py`中的`test_trigger()`函数，这一步会验证trigger是否正确触发，以及更新的结果是否正确。

__Checklist__：

1. 检查trigger是否建立成功
2. 更新rentalContract表中的数据，检查trigger是否正确触发，分别触发一次和五十次。
    - 随机rentalContract表中的数据，将dateOut修改为随机值。
    - 检查trigger_monitor表中的数据属和rentalContract表中rentalCost不为空记录数是否相等，即trigger是否触发和触发次数是否正确。
    - 检查renContract.rentalCost是否正确更新。

# Step 5 - View

执行`main.py`中的`test_view()`函数，验证view数据是否正确。
这里有个暗雷，view的字段没有一个可以做unique的，本程序使用customerId + modelName赌命，有问题可以从这里开始找。

__Checklist__：

1. 检查view是否建立成功。
2. 检查view数量是否等于有效数据数量。
3. 检查view每条数据计算是否正确。
4. 将部分Phone.IMEI更新为NULL，重新检查view数量是否等于有效数据数量以及检查view每条数据计算是否正确。

# PS

`main.py`中的`main()`函数继承了所有需要执行的子函数，可以直接用`main()`函数测试。

# NOTE

**超级无敌极品巨坑：**

sqlite, version 3.6.19开始支持外键。

**但是,**

启用外键约束只能作用于当前连接，一旦断开连接，外键约束就会失效，所以每次连接数据库都要重新启用外键约束。

```
PRAGMA foreign_keys = ON;
PRAGMA foreign_keys;
```
----
# 1402-sqlite-project Test Usage Method

# Step 1 - Replace Files

Replace the `.sql` files under the `/sql` folder with your own files.

# Step 2 - Create Database

Execute the `create_database()` function in `main.py`. This step will execute all the creation DDL statements and check if the basic table structure, constraints, and indexes are correct. At the same time, it will generate the trigger_monitor table to monitor the execution status of triggers and create another trigger: trigger_monitor to monitor the execution status of triggers in the project.

__Checklist__:

1. Successfully execute all .sql files without errors.
2. Create four tables: Phone, PhoneModel, rentalContract, Customer.
3. Check the basic table structure 
   - Phone table
      - Three fields: IMEI(TEXT), modelNumber(TEXT), modelName(TEXT).
      - Primary key: IMEI.
      - Foreign key: Phone.(modelNumber + modelName) -> PhoneModel.(modelNumber + modelName).
   - PhoneModel table
      - Six fields: modelNumber(TEXT), modelName(TEXT), storage(INTEGER), colour(TEXT), baseCost(REAL), dailyCost(REAL).
      - Primary key: modelNumber.
   - rentalContract table
      - Five fields: customerId(INTEGER), IMEI(TEXT), dateOut(TEXT), dateBack(TEXT), rentalCost(Real).
      - Primary key: customerId + IMEI + dateOut.
      - Foreign key: rentalContract.customerID -> Customer.customerID, rentalContract.IMEI -> Phone.IMEI.
   - Customer table
      - Three fields: customerId(INTEGER), customerName(TEXT), customerEmail(TEXT).
      - Primary key: customerId.

# Step 3 - Fake Data

Execute the `fake_data()` function in `main.py`. This step will generate data and insert it into the four tables created in the previous step. The table constraints will be validated again.

__Checklist__:

1. Check Primary Key
   - Randomly select a record from the Phone table, reinsert it into the Phone table, and check if there are any errors.
   - Randomly select a record from the PhoneModel table, reinsert it into the PhoneModel table, and check if there are any errors.
   - Randomly select a record from the rentalContract table, reinsert it into the rentalContract table, and check if there are any errors.
   - Randomly select a record from the Customer table, reinsert it into the Customer table, and check if there are any errors.
2. Check Foreign Key
   - Randomly select a record from the Phone table and modify its modelNumber to a value that does not exist in the PhoneModel table, and check if there are any errors. 
   - Randomly select a record from the Phone table and modify its modelName to a value that does not exist in the PhoneModel table, and check if there are any errors. 
   - Randomly select a record from the rentalContract table and modify its customerId to a value that does not exist in the Customer table, and check if there are any errors. 
   - Randomly select a record from the rentalContract table and modify its IMEI to a value that does not exist in the Phone table, and check if there are any errors.
3. Check 'Check Constraint'
   - Randomly select a record from the Phone table and truncate its IMEI to the first 7 digits, and check if there are any errors.
   - Randomly select a record from the Phone table and change the first 7 digits of its IMEI to random letters, and check if there are any errors.
   - Randomly select a record from the Phone table and add 1 to its IMEI, and check if there are any errors.

# Step 4 - Trigger

Execute the `test_trigger()` function in `main.py`. This step will verify if the triggers are correctly triggered and if the results of the updates are correct.

__Checklist__:

1. Check if the trigger was created successfully
2. Update the data in the rentalContract table and check if the trigger was triggered correctly, once and fifty times respectively.
   - Randomize the data in the rentalContract table by changing the dateOut to a random value.
   - Check whether the number of records in the trigger_monitor table and the number of records in the rentalContract table with non-null rentalCost are equal, i.e., whether the trigger is triggered and the number of times the trigger is triggered is correct.
   - Check if renContract.rentalCost is updated correctly.

# Step 5 - View

Execute the `test_view()` function in `main.py` to verify that the view data is correct.
There is a dark mine here, none of the fields of view can be made UNIQUE, this program uses customerId + modelName to gamble on its life, you can start looking here if you have problems.

__Checklist__:

1. check if the view is created successfully.
2. check if the number of views is equal to the number of valid data.
3. check if each data of the view is calculated correctly.
4. Update some Phone.IMEI to NULL, recheck if the view count is equal to the valid data count and verify if the calculation for each data in the view is correct.

# PS

The `main()` function in `main.py` inherits all the necessary sub-functions to be executed, so you can directly use the `main()` function for testing.

# NOTE

**SUPER INCREDIBLE EXTREMELY HUGE PIT: **

sqlite, version 3.6.19 started to support foreign keys.

**But,**

Enabling foreign key constraints only works for the current connection, once you disconnect, the foreign key constraints will be invalidated, so you have to re-enable the foreign key constraints every time you connect to the database.

```
PRAGMA foreign_keys = ON;
PRAGMA foreign_keys;
```
