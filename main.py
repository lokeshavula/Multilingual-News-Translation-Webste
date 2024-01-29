

def get_urls_topic(inp,pages):
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    URLS = []
    for pg in range(1,pages+1):
        url = f"https://thefederal.com/search?search={inp}&search_type=all&page={pg}"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content,"html.parser")
        for num,a in enumerate(soup.findAll("div",{"class":"col-md-12"})):
            for c in a.findAll("a",{"class":"img_para_text_hover"}):
                URLS.append("https://thefederal.com"+c.get("href"))
    return set(URLS)


def DataScreper_federal(inp,pages):
    try:
        import pandas as pd
        import requests
        from bs4 import BeautifulSoup
        URLS = get_urls_topic(inp,pages)
        F_data = {}
        for num,a1 in enumerate(URLS):
            # print(a1)
            f_data = {}
            f_data['url'] = a1 
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            req1 = requests.get(a1, headers=headers)
            soup1 = BeautifulSoup(req1.content,"html.parser")
            for b1 in soup1.findAll("h1",{"class":"font_bold article_two_cont_size py-xl-3 pt-2"}):
                f_data['title'] = b1.text.strip()
                 # print(b1.text.strip())
            for c1 in soup1.findAll("div",{"class":"detail_img_cover image_content_w img_only_hover"}):
                for d1 in c1.findAll("img",{"class":"img-fluid"}):
                    f_data['image'] = d1.get("src")
                    f_data['image_cap'] = d1.get("title")
            s = []
            S = ""
            for e1 in soup1.findAll("div",{"class":"entry-main-content dropcap"}):
                for f1 in e1.findAll("p"):
                    s.append(f1.text.strip())
                    S+=f1.text.strip()
                    f_data["all_data_list"] = s
                    f_data["all_data_para"] = S
            F_data[f"{inp}_A{num+1}"] = f_data
        return F_data
                
    except Exception as e:
        raise e


def translated_federal_data(lang,inp,pages):
    from googletrans import Translator
    translator = Translator()
    Data = DataScreper_federal(inp,pages)
    # print(Data)
    for i in Data:
        try:
            Data[i]["title"] = translator.translate(Data[i]["title"], dest = lang).text
            Data[i]["image_cap"] = translator.translate(Data[i]["image_cap"], dest = lang).text
            Data[i]["all_data_para"] = translator.translate(Data[i]["all_data_para"], dest = lang).text
            Z0 = []
            for j in range(len(Data[i]["all_data_list"])):
                Z0.append(translator.translate(Data[i]["all_data_list"][j], dest = lang).text)
            Data[i]["all_data_list"] = Z0
        except:
            continue
    return Data

t_data1 = translated_federal_data("ta","technology",1)
t_data1
