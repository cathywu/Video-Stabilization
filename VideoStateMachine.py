from RingBuffer import RingBuffer

class VideoStateMachine:
    def __init__(self,state):
        self.state = state
    def next_state(self,features,frame):
        self.state = self.state.transition(features,frame) or self.state
        return self.current_state()
    def current_state(self):
        return self.state

class VideoState:
    def __init__(self,features_history=None,
            frame_history=None):
        self.features_history = features_history or RingBuffer(size_max=10,default=None)
        self.frame_history = frame_history or RingBuffer(size_max=10,default=None)
        self.flow_history = RingBuffer(size_max=10,default=None)
    def transition(self,features,frame):
        self.features_history.write(features)
        self.frame_history.write(frame)
        if self.features_history.count > 1:
            diff = [(a-c,b-d) for ((a,b),(c,d)) in zip(self.features_history.get_prev(2),self.features_history.get_last())]
            x,y = zip(*diff)
            print "Current (%s,%s)" % (sum(x)/len(x),sum(y)/len(y))
        #recent_flowX.write(sum(x)/len(x))
        #recent_flowY.write(sum(y)/len(y))
        #print "Recent (%s,%s)" % (recent_flowX.meanmagnitude(),recent_flowY.meanmagnitude())
        return None
    def get_output_frame(self):
        return self.frame_history.get_last()

#class Shift10pxDownState(VideoState):

class NoiseState(VideoState):
    def __init__(self,flow_history=None,feature_history=None,
            frame_history=None):
        super(NoiseState,self).__init__(flow_history=flow_history,
                feature_history=feature_history,frame_history=frame_history)
    def transition(self,features,frame):
        super(NoiseState, self).transition(features,frame)

