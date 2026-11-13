'''协程入门'''
"""
在python3.5+中，协程通过async和await关键字实现
    使用async关键字定义的函数就是协程函数
    await是协程的灵魂，它用于暂停当前协程的执行，遇到await时，当前协程让出CPU控制权进入“挂起”状态
    事件循环（EventLoop）接管：他会去调度执行其他处于“就绪”状态的协程，等待对象完成后，事件循环会把控制权
    还给被挂起的协程，使其从await之后继续执行
    
await只能写在anync def内部，其作用是：
    遇到I0
    耗时操作(网络请求、接口调用、文件读写、数据库)时，暂停当前协程;
    把cPu控制权交还给事件循环;
    等I0操作完成后，事件循环再切回这个协程，从暂停处继续执行。
    
定义协程函数：
    async def 函数名():
        方法体
调用协程函数：
    asyncio.run(函数名)        #注意函数名带()
        
返回值：返回的是一个协程对象，虽然我们没有写return，但是协程函数也会自动返回协程对象
注意：如果想让当前协程挂起，让别的协程执行，需要使用await
"""
"""
线程：抢占式OS，强制切换不可控
程协：协作式主动await交出执行权可控

线程是操作系统管理的轻量级进程，抢占式切换开销大，有线程安全问题
协程是单线程内由代码调度的逻辑任务，仅await处切换，开销极低，无需加锁，IO高并发首选
"""

## 普通函数的执行流程：先进后出~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def func2():
    print('函数func2开始执行')
    print('函数func2执行完毕')


def func1():
    print('函数func1开始执行')
    func2()
    print('函数func1执行完毕')

if __name__ == '__main__':
    func1()

    print('①'*30)


#####################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
协程函数的执行机制：
    协程函数通过async和await关键字实现
    协程函数需要有单独的对象来负责执行（就像多线程执行顺序由CPU调度一样），即Event Loop（事件循环）
    事件循环作用：保存所有待执行协程；某个协程遇到阻塞立即切走，IO完成收到响应，再把协程放回就绪队列执行；自动来回切换多个携程单线程内并发
    
    协程函数本身不能直接决定调用（不能用常规的函数名()调用），直接调用协程函数会得到一个协程对象
"""

##导包
import asyncio
import time

##定义协程函数
async def func1():
    print('hello 协程函数')
    '''
    增加一个休眠动作
    time.sleep(2)     #之前学的休眠动作，属于线程级别的休眠，但是协程只有一个线程，若用了此命令，整个线程就停止了
        如果协程代码中包含，就会阻塞，等个事件循环和其他协程会被卡住，并发能力失效
    '''
    await asyncio.sleep(2)      #注意这里的休眠方式，与之前的方式不同
    #await为关键字； asyncio是包名； sleep是是协程函数，挂起2秒
    print('see you 协程函数')

if __name__ == '__main__':

    '''
    #func1()                  #按照以往的调用函数方式，会报错。多线程是由CPU调度的，多协程也应该有个调度者
    cor_obj = func1()
    print(cor_obj)           #直接调用不执行，只会得到一个协程对象
    print(type(cor_obj))     #输出结果为<class 'coroutine'>，即协程对象
    '''

    #正确的写法如下：
    asyncio.run(func1())      #将协程函数对象传入，相当于交给了Event Loop（协程管理员）
    ##asynci库提供run()工具，run()内部实例化一个EventLoop事件循环
    print('②'*30)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
★asyncio用法：
    asyncio.run()               #启动事件循环，异步函数
    asyncio.create_task()       #并发多个协程，把协程丢进事件循环后台调度，不用等一个结束再跑下一个
    asyncio.gather()            #批量接收一堆协程，统一等待所有任务完成，收集全部返回结果
    asyncio.sleep(秒数)          #异步休眠，模拟网络IO
    
网络IO = 你的程序通过网络“发请求”和“收响应”的过程。
"""

"""
同步：调用一个函数，必须等它完全执行完，才执行下一行代码。
异步：调用一个函数，它"告诉"你"我还没完，你先去做别的"，等它完了再通知你。
"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##1、协程函数同步(串行)执行的效果
async def work1(name,dealy):
    print(f'{name}开始执行')
    await asyncio.sleep(dealy)      #休眠的时间由参数传入
    print(f'{name}执行完毕')

async def main1():
    print('*******协程函数串行执行的耗时********')
    #awiat串行执行的关键，等待当前函数执行完后 再往下执行
    await work1('任务A',1)        #协程函数内，用await执行协程函数
    await work1('任务B',2)

if __name__ == '__main__':
    start = time.time()     #记录一下开始执行的时间
    asyncio.run(main1())
    end = time.time()        # 记录一下执行完毕的时间
    print(end-start)        #总耗时
#发现耗时3秒多一点，因为A任务和B任务耗时之和为3秒

print('③'*30)

## 2.协程函数异步（并行）执行的效果
'''
需要结合task以及gather()函数实现，
我们需要将协程任务封装成Task对象，通过create_task()函数
一旦封装成任务以后，协程函数会立即执行
'''
async def work2(name,dealy):
    print(f'{name}开始执行')
    await asyncio.sleep(dealy)      #休眠的时间由参数传入
    print(f'{name}执行完毕')
    return f'{name}任务的返回值'

async def main2():
    print('*******协程函数并行执行的耗时********')
    task_1 = asyncio.create_task(work2('任务A',1))
    task_2 = asyncio.create_task(work2('任务B',2))

    #将两个任务的返回值保存到result变量中
    result = await asyncio.gather(task_1,task_2)    #这里的await表示等待两个函数执行完毕后再获取结果
        # gather()函数表示等待两个任务都执行完毕，然后再获取返回值
    print(result)

"""
#上述另一种写法是：
async def main2():
    print('*******协程函数并行执行的耗时********')
    task_1 = asyncio.create_task(work2('任务A', 1))
    task_2 = asyncio.create_task(work2('任务B', 2))

    # 分别等待每个任务完成，获取返回值
    result_1 = await task_1
    result_2 = await task_2
    result = [result_1, result_2]  # 手动组装成列表
    print(result)
    
方式	                                        优点	                                适用场景
create_task + 分别 await	        可以逐个处理每个任务的结果	                    任务结果需要分别处理
asyncio.gather	                    代码简洁，统一等待	                      所有任务完成后再一起处理结果
"""

if __name__ == '__main__':
    start = time.time()     #记录一下开始执行的时间
    asyncio.run(main2())
    end = time.time()        # 记录一下执行完毕的时间
    print(end-start)        #总耗时
#发现耗时2秒多一点，因为A任务和B任务耗时较大的为2秒
##实际中的应用，比如浏览器中快速打开多个网页，不用等待一个网页加载完后再打开另一个，最终都会打开

"""
asyncio工作流程：
    1.async def定义协程函数;
    2.asyncio.run()开启事件循环;
    3.执行协程，遇到await暂停当前任务，让出线程;
    4.事件循环调度其他就绪协程执行;
    5.10操作完成，切回原协程继续执行剩余代码;
    6.所有协程执行完毕，关闭事件循环，程序退出。
"""


