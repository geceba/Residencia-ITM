from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm

class ModeloArima:

    def arima_modelo(valor_data, fecha_inicio='2018-10-09', fecha_fin='2018-11-02'):
        print(fecha_inicio)
        model = sm.tsa.statespace.SARIMAX(valor_data, xlim=[fecha_inicio, fecha_fin], order=(0,1,0), seasonal_order=(1,1,1,12))
        results = model.fit()
        #print(results.summary())


        return results
    
    def tendencia(results_predict, inicio=20, fin = 60):
        if(inicio == 0 and fin == 0):
            inicio = 20
            fin = 60
        return results_predict.predict(start= inicio, end = fin , dynamic= True)

   
        