import pandas as pd
from scipy import stats
import json
import math
from datetime import date
from settings.api_econom_code import get_data_shares

def api_calculate_two_shares(one_shares,two_shares,id_user):
    today = date.today()
    shares_company_one = get_data_shares(one_shares)
    shares_company_two = get_data_shares(two_shares)

    def get_two_itogs():
        itog_company_one =""
        itog_company_one+=f"Статистический анализ компании {one_shares}"+"\n"
        itog_company_one+=f'Среднее значение: {round(mean_one,2)}'+"\n"
        itog_company_one+=f'Медиана: {round(median_one,2)}'+"\n"
        itog_company_one+=f'Мода: {round(mode_one[0][0],2)}'+"\n"
        itog_company_one+=f'Стандартное отклонение: {round(std_dev_one,2)}'+"\n"
        itog_company_one+=f'Дисперсия для компании: {round(variance_one,2)}'

        itog_company_two =""
        itog_company_two+=f"Статистический анализ компании {two_shares}"+"\n"
        itog_company_two+=f'Среднее значение: {round(mean_two,2)}'+"\n"
        itog_company_two+=f'Медиана: {round(median_two,2)}'+"\n"
        itog_company_two+=f'Мода: {round(mode_two[0][0],2)}'+"\n"
        itog_company_two+=f'Стандартное отклонение: {round(std_dev_two,2)}'+"\n"
        itog_company_two+=f'Дисперсия: {round(variance_two,2)}'

        return itog_company_one, itog_company_two   
    
    def general_itog():
        itog = ""
        itog += f"Значение t-статистики: {round(t_stat,2)}"+"\n"
        x = p_value
        m, e = math.frexp(x)
        yx='{:.4f}*2^{}'.format(m, e)
        itog += f"p-value одновыборочного t-теста: {yx}"+"\n"

        if p_value < 0.05:
            itog += "Разница между двумя компаниями статистически значима."
            if mean_one > mean_two:
                itog += f"Может быть выгоднее вложиться в компанию {one_shares}."

            elif mean_two > mean_one:
                itog += f"Может быть выгоднее вложиться в компанию {two_shares}."
            else:
                itog += "Средние значения цен акций у обеих компаний равны."
        else:
            itog += "Разница между двумя компаниями не является статистически значимой."
        return itog
    
    # Создание DataFrame из массивов
    data = {'sco': shares_company_one, 'sct': shares_company_two}
    df = pd.DataFrame(data)

    # Расчет статистических показателей с помощью scipy.stats
    mean_one = df.sco.mean()
    median_one = df.sco.median()
    mode_one = stats.mode(df.sco, keepdims=True)
    std_dev_one = df.sco.std()
    variance_one = df.sco.var()

    mean_two = df.sct.mean()
    median_two = df.sct.median()
    mode_two = stats.mode(df.sct, keepdims=True)
    std_dev_two = df.sct.std()
    variance_two = df.sct.var()

    # Расчет t-статистики и p-value
    t_stat, p_value = stats.ttest_1samp(df.sco, df.sct.mean())

    # Проведение теста Уитни
    _, p_value = stats.mannwhitneyu(df.sco, df.sct, alternative='two-sided')

    itog_one, itog_two = get_two_itogs()
    main_itog = general_itog()


    # Создание словаря с результатами

    results = {
        "date": str(today),
        "company_one": {
            "name": one_shares,
            "stats": itog_one
        },
        "company_two": {
            "name": two_shares,
            "stats": itog_two
        },
        "analysis": main_itog
}
    
    # Записываем результаты в файл в формате JSON с использованием separators и pretty_print_stats
    with open(f"/BOTS/ECONOM_BOT/shares_data/analysis_{str(today)}_{id_user}_{one_shares}_vs_{two_shares}.json", "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, indent=2, ensure_ascii=False)
        
    return "Результаты готовы!"

def read_stats_from_json(one_shares,two_shares,id_user):
    today = date.today()
    with open(f"/BOTS/ECONOM_BOT/shares_data/analysis_{str(today)}_{id_user}_{one_shares}_vs_{two_shares}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    stats_one = data["company_one"]["stats"]
    stats_two = data["company_two"]["stats"]
    analysis = data["analysis"]

    return stats_one,stats_two,analysis

def read_json(name):
    with open(f"/BOTS/ECONOM_BOT/shares_data/{name}", "r", encoding="utf-8") as f:
        data = json.load(f)
    stats_one = data["company_one"]["stats"]
    stats_two = data["company_two"]["stats"]
    analysis = data["analysis"]

    return stats_one,stats_two,analysis