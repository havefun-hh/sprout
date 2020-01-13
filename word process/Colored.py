from colorama import init,Fore,Back,Style


class Colored_1(object):
    RED = '\033[31m'       #红色
    GREEN = '\033[32m'     #绿色
    YELLOW = '\033[33m'    #黄色
    BLUE = '\033[34m'      #蓝色
    FUCHSIA = '\033[35m'   #紫红色
    CYAN = '\033[36m'      #青蓝色
    WHITE = '\033[37m'     #白色
    #：no color
    RESET = '\033[0m'      #终端默认颜色
    RED_YELLOW = '\033[1;31;43m'     #字体红色，背景黄色
    BRIGHT_BLUE = '\033[1;35;36m'    #亮蓝色
    def color_str(self, color, s):
        return '{}{}{}'.format(getattr(self,color),s,self.RESET)
    
    def red(self, s):
        return self.color_str('RED', s)
    
    def green(self, s):
        return self.color_str('GREEN', s)
    
    def yellow(self, s):
        return self.color_str('YELLOW', s)
    
    def blue(self, s):
        return self.color_str('BLUE', s)
    
    def fuchsia(self, s):
        return self.color_str('FUCHSIA', s)
    
    def cyan(self, s):
        return self.color_str('CYAN', s)
    
    def white(self, s):
        return self.color_str('WHITE', s)
    
    def red_yellow(self, s):
        return self.color_str('RED_YELLOW', s)
    
    def bright_blue(self, s):
        return self.color_str('BRIGHT_BLUE', s)

class Colored_2(object):
    def red(self, s):
        return Fore.RED + s + Fore.RESET
    
    def green(self, s):
        return Fore.GREEN + s + Fore.RESET
    
    def yellow(self, s):
        return Fore.YELLOW + s + Fore.RESET
    
    def blue(self, s):
        return Fore.BLUE + s + Fore.RESET
    
    def magenta(self, s):
        return Fore.MAGENTA + s + Fore.RESET
    
    def cyan(self, s):
        return Fore.CYAN + s + Fore.RESET
    
    def white(self, s):
        return Fore.WHITE + s + Fore.RESET
    
    def balck(self, s):
        return Fore.BLACK
    
    def white_green(self, s):
        return Fore.WHITE + Back.GREEN + s + Fore.RESET + Back.RESET
    
    def white_red(self, s):  #实际显示为橙色
        return Fore.WHITE + Back.RED + s + Fore.RESET + Back.RESET
    
    def white_yellow(self, s):  #实际显示为橙色
        return Fore.WHITE + Back.YELLOW + s + Fore.RESET + Back.RESET
    
    def white_blue(self, s):  #实际显示为深蓝色
        return Fore.WHITE + Back.BLUE + s + Fore.RESET + Back.RESET
    
    def white_magenta(self, s):  #实际显示为紫色
        return Fore.WHITE + Back.MAGENTA + s + Fore.RESET + Back.RESET
        
    def white_cyan(self, s):  #实际显示为浅蓝色
        return Fore.MAGENTA + Back.CYAN + s + Fore.RESET + Back.RESET
    

# #-----------使用示例如下--------
# color = Colored_1()
# print(color.red('I am red!'))
# print(color.green('I am green!'))
# print(color.yellow('I am yellow!'))
# print(color.blue('I am blue!'))
# print(color.fuchsia('I am fuchsia!'))
# print(color.cyan('I am cyan!'))
# print(color.white('I am white!'))
# print(color.red_yellow('test'))
# print(color.bright_blue('test'))

# color = Colored_2()
# print(color.red('I am red!'))
# print(color.green('I am green!'))
# print(color.yellow('I am yellow!'))
# print(color.blue('I am blue!'))
# print(color.magenta('I am magenta!'))
# print(color.cyan('I am cyan!'))
# print(color.white('I am white!'))
# print(color.white_green('I am white green!'))
# print(color.white_yellow('test1!'))
# print(color.white_yellow('test2!'))
# print(color.white_blue('test3!'))
# print(color.white_magenta('test4!'))
# print(color.white_cyan('test5!'))


#--------------------------------
#显示格式：\033[显示方式;前景色;背景色m
#--------------------------------
#显示方式           说明
#   0             终端默认设置
#   1             高亮显示
#   4             使用下划线
#   5             闪烁
#   7             反白显示
#   8             不可见
#   22            非粗体
#   24            非下划线
#   25            非闪烁
#
#前景色            背景色          颜色
#  30                40            黑色
#  31                41            红色
#  32                42            绿色
#  33                43            黄色
#  34                44            蓝色
#  35                45            紫红色
#  36                46            青蓝色
#  37                47            白色
#---------------------------------------


