#!/usr/bin/python

class Observation:
    """
    object to accumulate signal observations into a sample
    """
    def __init__(self, sig_str,isAP=False, avgsize=30, bytes=0):
        #self.ss_sum = sig_str
        #self.ss_sum_squares = sig_str^2
        #self.AP = isAP
        #self.bytes_sum = bytes
        self.count=1
        self.avgsize=avgsize    # no of obs for rolling average
        self.rolling_samples = []
        self.localcount=0

    def is_number(str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def getlocalcount(self):
        """
        everytime value is read reset to zero. incr by add (signal sample)
        """
        result = self.localcount
        self.localcount=0
        return result


    def add(self, sig_str, bytes=0):
        #if is_number(sig_str):
        if len(sig_str)>0:
            self.localcount+=1
            #for rolling average keep last avgsize samples 
            if len(self.rolling_samples) < self.avgsize:
                self.rolling_samples.append(int(sig_str))
            else:
                self.rolling_samples.pop(0)
                self.rolling_samples.append(int(sig_str))
            self.localcount+=1

   # def avg_sig(self):
    #    return   self.ss_sum / self.count

    #std variance of sample = E[x^2] - (E[x])^2
    #def var_sig(self):
    #    return (self.ss_sum_squares/self.count - self.avg_sig()^2)
#

    def rolling_avg(self):
        size=float(len(self.rolling_samples))
        if size>0:   
            return float(sum(self.rolling_samples)/size)
        else:
            return 0

    def rolling_var(self):
      if (len(self.rolling_samples) == 0):
        return 0
      xbar=float(self.rolling_avg())
      var = ([ (x - xbar) for x in self.rolling_samples])
      var = [ x*x for x in var] 
      var = sum(var)/float(len(self.rolling_samples))
      return var 
      #  sumsquares = sum([ x^2 for x in self.rolling_samples])
      #  denom =  len(self.rolling_samples) - self.rolling_avg()^2
      #  if (denom == 0):
      #      return 0
      #%  else:
      #      return sumsquares/denom
