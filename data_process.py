import re
import string
from unicodedata import normalize
from numpy.ma import array

FILE_PATH = 'raw_data/cmn.txt'

#1、以utf-8格式加载文件.
#open() 方法用于打开一个文件，并返回文件对象
#open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
#file: 必需，文件路径（相对或者绝对路径）。
#mode: 可选，文件打开模式
#buffering: 设置缓冲
#encoding: 一般使用utf8
#errors: 报错级别
#newline: 区分换行符
#closefd: 传入的file参数类型
#file.read([size])  从文件读取指定的字节数，如果未给定或为负则读取所有。
def load_doc(filename):
  file = open(filename, mode='rt', encoding='utf-8')
  text = file.read()
  file.close()
  return text


#2、逐行分割加载的文本，然后按短语分割。
#strip() 方法用于移除字符串头尾指定的字符（默认为空格）或字符序列
#str.split(str="", num=string.count(str))
#通过指定分隔符对字符串进行切片，如果第二个参数 num 有指定值，则分割为 num+1 个子字符串。
def to_pairs(doc):
  #lines 从doc中解析的所有字符串行
  lines = doc.strip.split('\n')
  #pairs 每行里的中英文字符串对
  pairs = [line.split('\t') for line in lines]
  return pairs

#3、删除特殊字符来清理句子,返回清理后的中英文对数组
#string.printable 所有可打印的字符集，包含数字，字母，标点空白符
#string.punctuation：找出字符串中的所有的标点
#re.escape(pattern)可以对文本(字符串)中所有可能被解释为正则运算符的字符进行转义，返回一个字符串, 其中的所有非字母数字字符都带有反斜杠
#compile(pattern [, flags]) ，该函数根据包含的正则表达式的字符串创建模式对象。可以实现更有效率的匹配
#'abc'表示字符串中有'abc'就匹配成功  '[abc]'表示字符串中有'a'或'b'或'c'就匹配成功  '^abc'表示字符串由'abc'开头就匹配成功
#'^[abc]'表示字符串由'a'或'b'或'c'开头的  '[^abc]'表示匹配'a','b','c'之外的字符。如果一个字符串是由'a','b','c'组合起来的，那就是假 
# 当^表示取反的时候，只有一种情况，就是在中括号里面，而且是每一个字符之外的。
def clean_pairs(pairs):
  cleaned_pairs = list()
  re_print = re.compile([^%s] % re.escape(string.printable))
  
  #Python maketrans() 对于接受两个参数的最简单的调用方式，第一个参数是字符串，表示需要转换的字符，第二个参数也是字符串，表示转换的目标。两个字符串的长度必须相同，为一一对应的关系。
  #在Python3中可以有第三个参数，表示要删除的字符，也是字符串。返回一个字符映射转换表供 translate() 方法调用
  table = str.maketrans('', '', string.punctuation)
  for pair in pairs:
    cleaned_pair = list()
    for line in pair:
      # normalize unicode characters
      line = normalize('NFD', line).encode('ascii', 'ignore')
      line = line.decode('UTF-8')
      line = line.split()
      line = [word.lower() for word in line]
      line = [word.translate(table) for word in line]
      line = [re_print.sub('', w) for w in line]
      line = [word for word in line if word.isalpha()]
      cleaned_pair.append(' '.join(line))
    cleaned_pairs.append(cleaned_pair)
  
  return array(cleaned_pairs)

min_line_length = 2   #一句话最少需要的单词数
max_line_length = 30  #一句话最多允许的单词数
frequence_of_word = 1 #词最少出现的次数


#4、创建单词索引和反向单词索引（从单词→id和id→单词映射的字典）

#读取文件，以多行的形式返回
def read_file_to_lines(filename)
  lines = open(filename).read().split('\n')
  return lines

# Create a dictionary for the frequency of the vocabulary。返回词典（词：出现次数）
# 小括号( )：代表tuple元组数据类型，元组是一种不可变序列；中括号[ ]，代表list列表数据类型；
# 大括号{ }花括号：代表dict字典数据类型，字典是由键对值组组成。冒号':'分开键和值，逗号','隔开组
#split() 通过指定分隔符对字符串进行切片,分隔符，默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等
def create_dictionary_word_usage(selected_source, selected_target)
  vocab = {}
  for source in selected_source:
    for word in source.split():
      if word not in vocab:
        vocab[word] = 1
      else:
        vocab[word] += 1
      
  for target in selected_target:
    for word in target.split():
      if word not in vocab:
        vocab[word] = 1
      else:
        vocab[word] += 1
     
  return vocab

# word 到 id 的映射
def vocab_from_word_to_emb(dict_word_usage, min_number_of_usage):
  vocab_word_to_int = {}
  
  vocab_word_to_int['<GO>'] = 0
  vocab_word_to_int['<EOS>'] = 1
  vocab_word_to_int['<UNK>'] = 2
  vocab_word_to_int['<PAD>'] = 3
  
  word_num = 4
  for word, count in dict_word_usage.items():
    # maximum number of characters allowed in a word is 20
    if len(word) <= 20:
      if count >= min_number_of_usage:
        vocab_word_to_int[word] = word_num
        word_num += 1
        
  return vocab_word_to_int

#按行写入文件
def write_lines_to_file(filename, list_of_lines):
  with open(filename, 'w') as file_to_write:
    for i in range(len(list_of_lines)):
      file_to_write.write(list_of_lines[i] + "\n")

#将词典写入文件
def write_dict_to_file(filename, dict_to_write):
  with open(filename, 'w') as file_to_write:
    for key, value in dict_to_write.items():
      file_to_write.write(str(key) + "=" + str(value) + "\n")


#根据短句内词的个数，从小到大排序
#enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。
def sort_text_based_on_number_of_words(sources, targets)
  sorted_sources = []
  sorted_targets = []
  
  for length in range(min_line_length, max_line_length):
    #比较source词的长度（单词数量）
    #enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。
    #split 返回分割后的字符串列表,用空格做分隔符可以得到单词个数
    for i, ques in enumerate(source):
      que_arry = ques.split(" ")
      if len(que_arry) == length:
        sorted_sources.append(sources[i])
        sorted_targets.append(targets[i])
        
  return sorted_sources, sorted_targets
    

#清理多行句子
def clean_sentence(sentences):
  cleaned_sentences = []
  for sentence in sentences:
    sentence = clean_text(sentence)
    cleaned_sentences.append(sentence)
  return cleaned_sentences

#清理一行句子
#'''Clean text by removing unnecessary characters and altering the format of words.'''
def clean_text(text):
  
  #转成小写
  text = text.lower()
  
  text = re.sub(r"i'm", "i am", text)
  text = re.sub(r"he's", "he is", text)
  text = re.sub(r"she's", "she is", text)
  text = re.sub(r"it's", "it is", text)
  text = re.sub(r"that's", "that is", text)
  text = re.sub(r"what's", "what is", text)
  text = re.sub(r"where's", "where is", text)
  text = re.sub(r"\'ll", " will", text)
  text = re.sub(r"\'ve", " have", text)
  text = re.sub(r"\'re", " are", text)
  text = re.sub(r"\'d", " would", text)
  text = re.sub(r"won't", "will not", text)
  text = re.sub(r"can't", "cannot", text)
  text = re.sub(r"n't", " not", text)
  text = re.sub(r"n'", "ng", text)
  text = re.sub(r"\'bout", " about", text)
  text = re.sub(r"\'til", " until", text)
  text = re.sub(r"temme", "tell me", text)
  text = re.sub(r"gimme", "give me", text)
  text = re.sub(r"howz", "how is", text)
  text = re.sub(r"let's", "let us", text)
  text = re.sub(r" & ", " and ", text)
  text = re.sub(r"[-()\"#[\]/@;:<>{}`*_+=&~|.!/?,]", "", text)
  
  return text

#将pairs分别保存为用于训练的source和target文件，返回有效的训练对数量
def create_source_target_file_from_paris(paris, source_file, target_file, min_words, max_words):
  source_file = open(source_file, 'w', newline='\n', encodeing='utf-8')
  target_file = open(target_file, 'w', newline='\n', encodeing='utf-8')
  #有效的训练对数量
  number_of_samples = 0
  for line in pairs:
    number_of_words_source = len(line[0])
    number_of_words_target = len(line[1])
    #满足长度的中英词对，保存英文短语到source文件，保存中文短语到target文件
    if (number_of_words_source >= min_words and number_of_words_source <= max_words
       and number_of_words_target >= min_words and number_of_words_target <= max_words):
      source_file.write(line[0])
      source_file.write('\n')
      target_file.write(line[1])
      target_file.write('\n')
      number_of_samples += 1
      
    source_file.close()
    target_file.close()
    return number_of_samples
  
  
#数据处理主函数
def main_prepare_data():
  #读文件
  
  
  #得到英文-中文短语对
  
  
  #根据英中文对，得到 翻译原(英文)文件 和 翻译目标(中文)文件
  
  
  #分别读取翻译原文件 和 翻译目标文件 为多行句子
  
  
  #清理句子，删除特殊字符 （清理翻译原文件和翻译目标文件中的多行句子）
  
  
  #得到词-id映射关系
  
  
  #保存词-id映射到文件
  
  
  #根据词长度排序
  
  #保存排序后的中英文训练文件
  
  

    
