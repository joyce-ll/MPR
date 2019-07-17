#from preprocessor import Preprocessor
import math

###queue for expanding and breadth-searching
class CircularQueue:
    def __init__(self,n=100):   #n=len(Preprocessor.points)
        self.size=n
        self.s=[None for i in range(0,self.size)]
        self.front=0
        self.rear=0

    def enqueue(self,x):
        if (self.rear+1)%self.size!=self.front:
            self.rear=(self.rear+1)%self.size
            self.s[self.rear]=x
        else:
            print("full")

    def dequeue(self):
        if self.s==None:
            print("empty")
            return
        else:
            self.front=(self.front+1)%self.size
            return self.s[self.front]

Po=[]   #路径点 Po=Preprocessor.points

class Point:
    def __init__(self,latitude,longitude,classfied=False):
        self.latitude=latitude
        self.longitude=longitude
        self.classfied=classfied

###参数
alpha=5
theta=math.pi/2   #方向角度差
delta=200   #比例因数
t=0.5   #一致性
fi=3   #簇大小

#####transfer network
class Transfer_Network:
    def __init__(self):
        self.nodes=[]
        self.edges=[]

    # 欧式距离
    def dist(self,p,q):
        return ((p[0]-q[0])**2+(p[1]-q[1])**2)**0.5

    # coh(p,q)
    def coh(self,p,q,alpha=5,beta=2,theta=math.pi/2,delta=200):
        return (math.exp(-((self.dist(p,q)/delta)**alpha)))*((abs(math.sin(theta)))**beta)

    # transfer node
    def create_transfer_node(self):
        clusters=self.coherence_expanding()
        for cluster in clusters:
            sum1,sum2=0,0
            for point in cluster:
                sum1+=point.latitude
                sum2+=point.longitude
            node=Point(sum1/len(cluster),sum2/len(cluster))
            self.nodes.append(node)
            #how to represent transfer edge???

    # 由各点形成的簇
    def coherence_expanding(self):
        clusters = []
        for p in Po:
            if p.classfied == False:
                p.classfied = True
                cluster = self.expand(p)
                if len(cluster) >= fi:
                    clusters.append(cluster)
        return clusters

    # 由点p扩张
    def expand(self,p):
        seeds = CircularQueue()  # 临时存储 队列长度最多为点的总个数
        result = []
        seeds.enqueue(p)
        result.append(p)
        while seeds != None:
            seed = seeds.dequeue()
            points = self.RangeQuery(seed)   #seed为圆心 radius为半径 以内的所有点
            for i in range(len(points)):
                pt = points[i]
                if pt.classfied == False and self.coh(seed, pt) >= t:
                    seeds.enqueue(pt)
                    result.append(pt)
        return result

    def RangeQuery(self,seed):
        range_query = []
        for p in Po:
            if self.dist(p,seed) <= delta*((-math.log(t))**(1/alpha)):
                range_query.append(p)
        return range_query

TN=Transfer_Network()
N=TN.nodes   #transfer nodes
E=TN.edges   #transfer edges
