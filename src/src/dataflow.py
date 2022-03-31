from math import perm


class dataflow:
    def __init__(self, mac=None, mems=[], flow_params=[], permut=[], data={}):
        self.mac = mac
        self.mems = mems       
        self.K1 = 0
        self.P1 = 0
        self.R1 = 0
        self.K2 = 0
        self.P2 = 0
        self.R2 = 0
        self.K  = 0
        self.P  = 0
        self.R  = 0
        self.permut = permut
        self.set_params(flow_params)
        self.data=data

    def set_params(self, flow_params=[]):
        if len(flow_params) == 6:
            self.K1 = flow_params[0]
            self.P1 = flow_params[1]
            self.R1 = flow_params[2]
            self.K2 = flow_params[3]
            self.P2 = flow_params[4]
            self.R2 = flow_params[5]
            self.K = self.K1 * self.K2
            self.P = self.P1 * self.P2
            self.R = self.R1 * self.R2        

    def do_sim(self, I, permut):
        init_o = [] 

        i = [0,0,0,0,0,0]

        ## MAIN MEM ##
        i[0] = 0
        while i[0] < I[0]:
            i[1] = 0
            while i[1] < I[1]:
                i[2] = 0
                while i[2] < I[2]:
                    ## GLOB BUFF ##
                    i[3] = 0
                    while i[3] < I[3]:
                        i[4] = 0
                        while i[4] < I[4]:
                            i[5] = 0
                            while i[5] < I[5]:
                                k1 = i[permut['k1']]
                                k2 = i[permut['k2']]
                                p1 = i[permut['p1']]
                                p2 = i[permut['p2']]
                                r1 = i[permut['r1']]
                                r2 = i[permut['r2']]

                                k = k1 * self.K2 + k2

                                p = p1 * self.P2 + p2

                                if self.R2 > 1:
                                    r = r1 * self.R2 + r2
                                else:
                                    r = r1

                                if self.data['o'][k][p] not in init_o:
                                    ## INIT O[k][p] ##
                                    self.mems[1].write(self.data['o'][k][p])
                                    init_o.append(self.data['o'][k][p])
                                else:
                                    self.mems[1].read(self.data['o'][k][p])

                                self.mems[1].read(self.data['i'][p+r])
                                self.mems[1].read(self.data['f'][k][r])

                                self.mac.calculate()     

                                self.mems[1].write(self.data['o'][k][p])

                                i[5] += 1                       
                            i[4] +=1
                        i[3] += 1
                    i[2] += 1
                i[1] += 1
            i[0] += 1

        for data in self.mems[1].data['o']:
            self.mems[0].write(data)
