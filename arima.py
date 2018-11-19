from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm

class ModeloArima:

    def arima_modelo(valor_data):
        model = sm.tsa.statespace.SARIMAX(valor_data, xlim=['2018-10-09', '2018-11-02'], order=(0,1,0), seasonal_order=(1,1,1,12))
        results = model.fit()
        #print(results.summary())

        return results
    
    def tendencia(results_predict):
        return results_predict.predict(start= 20, end =60 , dynamic= True)

   
        