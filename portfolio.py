import yfinance as yf
import time
import threading

class stock():
    def __init__(self,ticker,price,qty):
        self.ticker=ticker
        self.price=price
        self.qty=qty

    def current_value(self,current_price):
        self.current_price=current_price 
        return print(self.current_price*self.qty)
    
    def profit_pct(self):
        return print(self.current_price*self.qty - self.price*self.qty)

class Portfolio():
    def __init__(self,owner_name):
        self.kasa = 0.0
        self.owner_name= owner_name
        self.liste=[]
    def addstock(self,stock):
        self.liste.append(stock)
    def sell_stock(self, ticker, qty):
        for s in self.liste:
            if s.ticker == ticker:
                if qty > s.qty:
                 print("Yetersiz adet.")
                 return
                s.qty -= qty
                self.kasa += qty * s.current_price 
                if s.qty == 0:
                    self.liste.remove(s)
                    print(f"{ticker} portföyden çıkarıldı.")
                else:
                    print(f"{qty} adet satıldı. Kalan: {s.qty}")
                return
        print("Hisse bulunamadı.")
          
    def remove_stock(self,ticker):
        for s in self.liste:
            if s.ticker==ticker:
                self.liste.remove(s)
                print("Başarıyla kaldırıldı")
                return
        print("Hisse bulunamadı.")    

    def total_invested(self):
        total=0
        for s in self.liste:
            total+= s.price*s.qty
        print("Toplam yatiriminiz:",total)      
    def total_current_value(self):
        total2=0
        for s in self.liste:
            total2+= s.current_price*s.qty
        print("Yatırımınızın Anlık Degeri:",total2)
    def total_profit_loss(self):
        profit2=0
        for s in self.liste:
            profit2+=s.current_price*s.qty - s.price*s.qty
        print("Toplam Karınız:",profit2)
    def show_portfolio(self):
     print("-" * 50)
     print(f"{self.owner_name} Portföyü")
     print("-" * 50)
     for s in self.liste:
        print(f"{s.ticker} | {s.qty} adet | Alış: {s.price} | Güncel: {s.current_price} | K/Z: {s.current_price*s.qty - s.price*s.qty:.2f} $")
     print("-" * 50)
     self.total_invested()        
     self.total_current_value()
     self.total_profit_loss() 
     print(f"Kasa: {self.kasa:.2f} $")
     print("-" * 50)

def fiyat_guncelle(portfoy):
    while True:
        for s in portfoy.liste:
            t = yf.Ticker(s.ticker)
            s.current_price = t.fast_info['last_price']
        time.sleep(60)

def main():
    isim = input("Adın ne? ")
    portfoy = Portfolio(isim)
    t = threading.Thread(target=fiyat_guncelle, args=(portfoy,), daemon=True)
    t.start()
    while True:
        print("\n1) Hisse ekle")
        print("2) Hisse çıkar")
        print("3) Portföyü göster")
        print("4) Çıkış")
        secim = input("Seçim: ")
        if secim == "1":
         ticker = input("Ticker: ").upper()
         price = float(input("Alış fiyatı: "))
         qty = int(input("Adet: "))
         yeni_hisse = stock(ticker, price, qty)
         t = yf.Ticker(ticker)
         yeni_hisse.current_price = t.fast_info['last_price'] 
         portfoy.addstock(yeni_hisse)
         print(f"{ticker} eklendi. Anlık fiyat: {yeni_hisse.current_price}$")
        elif secim == "2":
         ticker = input("Ticker: ").upper()
         qty = int(input("Kaç adet satmak istiyorsun? "))
         portfoy.sell_stock(ticker, qty)
        elif secim == "3":
         portfoy.show_portfolio() 
        elif secim == "4":
         break   

if __name__ == "__main__":
    main()