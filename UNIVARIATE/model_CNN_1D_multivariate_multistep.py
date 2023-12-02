import TimeSeriesPreparation as tsp
from keras.models import Sequential, save_model
from keras.layers import Dense, Conv1D,MaxPooling1D,Flatten




class ModelTest():
    def __init__(self):
        self.data =  tsp.DataPreparation()
        self.Configs = tsp.json.load(open('Config_model_CNN1D.json', 'r'))
        self.batch_size = self.Configs['CONFIG_DATA']['batch_size']
        self.interest_feature = self.Configs['CONFIG_DATA']['interest_feature']
        self.n_steps_in = self.Configs['CONFIG_DATA']['n_steps_in']
        self.n_steps_out = self.Configs['CONFIG_DATA']['n_steps_out']
        self.epochs = self.Configs['CONFIG_DATA']['epochs']



    def ModelGen(self):

        data =   tsp.DataPreparation()
        X,y, n_steps,interest_feature = data.data_preparation_multistep(self.batch_size,self.interest_feature,self.n_steps_in, self.n_steps_out)
        X = X.reshape((X.shape[0], X.shape[1], interest_feature))
 
        n_output = y.shape[1]*y.shape[2]
        y = y.reshape((y.shape[0], n_output))

        # define model
        model = Sequential()
        model.add(Conv1D(64,self.n_steps_in , activation='relu', input_shape=(n_steps, interest_feature)))
        model.add(MaxPooling1D(pool_size=2, strides=2,padding='same'))
        model.add(Flatten())
        model.add(Dense(60, activation='relu'))
        model.add(Dense(n_output))
        model.compile(optimizer='adam', loss='mse')
        # fit model
        model.fit(X, y, epochs=self.epochs, verbose=0)
        # save model
        save_model(model, 'model_CNN_1D_mv_ms.h5')
    
        
      
       




ciao = ModelTest()
ciao.ModelGen()