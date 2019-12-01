# Notes
### 1) Preparing data
* trojke: "Danes sije sonce. Jutri bom bolan."
    1) es_, s_s, _si (best)
    2) sij, ije, son (good)
    3) ess, ssi, sij (ta odpade)
    
* ločila: 
    1) zamenjamo s presledkom
    2) samo en presledek
    3) s = s.replace(".", " ") (mora bit = )
    
* velike / male:
    1) vse enako: zmanjšamo šum, zgubimo info (če ne obratno)
    2) s = s.lower()

### 2) Reading data
* struktura:
    1) dictionary dictionary int
    
### 3) Računanje podobnosti
* kosinusna podobnost:
    1) cos(x*y) = skalarni produkt med vektorjema / produkt doklžin vektorjev
    2) x * y = x1y1 + x2y2 + x3y3
    3) |x| = sqrt(x1^2 + x2^2 ...)
* različni atributi:
    1) vzamemo samo tiste ki so skupni
    2) zgorej samo skupne
    3) spodej vse za x in vse za y
* unidecode:
    1) pretvarja v navadne crke
    2) to naredimo takoj po branju
    3) ni idealna
    
### 4) Gručenje
* k means (to bo na izpitu):
    1) naključno izberemo k voditeljev
    2) kateri elementi so najbližje tem voditeljem -> skupine
    3) premaknem voditelja skupine v središče skupine
    4) ponavljamo dokler se skupine spreminjajo
    
* k medoids:
    1) voditelj mora biti vedno eden izmed elementov
    2) (mediana 3, mean 3.666)
    3) nemoremo računati centra gruče, ker niso vsi atributi skupni
    4) postopek:
        1) naključno izberemo k voditeljev
        2) kateri elementi so najbližje tem voditeljem -> skupine
        3) za vsak element seštet vse razdalje do ostalih -> minimum je voditelj
        4) ponavljamo dokler se skupine ne spreminjajo
        5) (če se vsi voditelji ohranijo je tudi kul)
    5) k-means, vendar zaradi podatkov vedno element

### 5) Silhueta
* silhueta primerja razdalje v trenutnem s v najbližjem drugim
* preverja kvaliteto clustering za posamezen element
* število pojavitev / verjetnost v histogramu
* kolikokrat se je pojavila neka vrednost silhuete
* matplotlib.hist(ogram)
    
### *) Extra
Vaje bodo namesto predavanj.