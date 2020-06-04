import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import BytesIO
import base64

def load_telco():
    # Read data
    telco = pd.read_csv('data/telcochurn.csv')
    
    # Adjust dtypes
    catcol = telco.select_dtypes('object').columns
    telco[catcol] = telco[catcol].apply(lambda x: x.astype('category'))
    
    # Tenure Months to grouping categories
    def grouping_tenure(telco) :
        if telco["tenure_months"] <= 12 :
            return "< 1 Year"
        elif (telco["tenure_months"] > 12) & (telco["tenure_months"] <= 24):
            return "1-2 Year"
        elif (telco["tenure_months"] > 24) & (telco["tenure_months"] <= 48) :
            return "2-4 Year"
        elif (telco["tenure_months"] > 48) & (telco["tenure_months"] <= 60) :
            return "4-5 Year"
        else:
            return "> 5 Year"
        
    telco["tenure_group"] = telco.apply(lambda telco: grouping_tenure(telco), axis = 1)
    
    # Adjust category order
    tenure_group = ["< 1 Year", "1-2 Year", "2-4 Year", "4-5 Year", "> 5 Year"]
    telco["tenure_group"] = pd.Categorical(telco["tenure_group"], categories = tenure_group, ordered=True)
    
    return(telco)

def table_churn(data):
    table = pd.crosstab(
    index = data['churn_label'],
    columns = 'percent',
    normalize = True)*100
    return(table)

def plot_phone(data):
    
    # ---- Phone Service Customer
    phone = pd.crosstab(
    data['phone_service'], data['churn_label']
    )
  
    ax = phone.plot(kind = 'barh', color=['#53a4b1','#c34454'], figsize = (8,6))

    # Plot Configuration
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.axes().get_yaxis().set_label_text('')
    plt.title('Phone Service Customer')
    
    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_internet(data):

    # ---- Internet Service Customer
    inet = pd.crosstab(
    data['internet_service'], data['churn_label'],
    normalize=True
    )*100

    ax = inet.plot(kind = 'barh', color=['#53a4b1','#c34454'], figsize = (8,6))

    # Plot Configuration
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.axes().get_yaxis().set_label_text('')
    plt.title('Internet Service Customer')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_tenure_churn(data):
    
    # ---- Churn Rate by Tenure Group
    churnrate = pd.crosstab(
    data['tenure_group'], data['churn_label']
    ,normalize='columns'
    )*100

    ax = churnrate.plot(kind = 'bar', color=['#53a4b1','#c34454'], figsize=(8, 6))

    # Plot Configuration
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.axes().get_xaxis().set_label_text('')
    plt.xticks(rotation = 360)
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.title('Churn Rate by Tenure Group')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_tenure_cltv(data):

    # ---- Average Lifetime Value by Tenure
    tenure_agg = data.groupby(['tenure_months','churn_label']).agg({"cltv":"mean"})
    tenure_agg.reset_index(inplace=True)
    tenure_agg = tenure_agg.pivot(index='tenure_months', columns='churn_label', values= 'cltv')
    tenure_agg
    ax = tenure_agg.plot(color=['#333333','#b3b3b3'], figsize=(8, 6),style = '.--')

    # Plot Configuration
    plt.axes().get_xaxis().set_label_text('Tenure (in Months)')
    plt.title('Average Lifetime Value by Tenure')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    plt.xticks(rotation = 360)
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_customer_churn(data):

    # ---- Churn Rate by Customer Per Tenure Group
    cond = data['churn_label'] == "Yes"
    churn = data[cond]
    churn

    churnratebygender = pd.crosstab(
        churn['tenure_group'], churn['gender']
        ,normalize='index'
    )*100
    churnratebygender

    # Plot Configuration
    ax = churnratebygender.plot(color=['#333333','#b3b3b3'], figsize=(8, 6),style = '.--')

    # ax.xaxis.set_major_formatter(mtick.FixedFormatter('%x'))
    # ax.xaxis.set_major_formatter
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    # ax.xaxis.set_major_formatter(mtick.FormatStrFormatter())
    plt.axes().get_xaxis().set_label_text('Tenure Group')
    plt.xticks(rotation = 360)
    plt.legend(['Female', 'Male'],fancybox=True,shadow=True)
    plt.title('Churn Rate by Gender per Tenure Group')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)
