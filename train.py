from LAC import LAC

def seg_train():
    # 选择使用分词模型
    lac = LAC(mode='seg')

    # # 训练和测试数据集，格式一致
    # train_file = "./data/seg_train.tsv"
    # test_file = "./data/seg_test.tsv"
    # lac.train(model_save_dir='./task1_data/my_seg_model/',train_data=train_file, test_data=test_file)
    #
    # # 使用自己训练好的模型
    # my_seg = LAC(model_path='seg')
    return lac

def lac_train():
    # 选择使用默认的词法分析模型
    lac = LAC(mode='lac')
    # # 训练和测试数据集，格式一致
    # train_file = "./data/lac_train.tsv"
    # test_file = "./data/lac_test.tsv"
    # lac.train(model_save_dir='./task1_data/my_lac_model/', train_data=train_file, test_data=test_file)
    # # 使用自己训练好的模型
    # my_lac = LAC(model_path='lac')
    return lac
