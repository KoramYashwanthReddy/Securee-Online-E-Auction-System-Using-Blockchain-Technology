from flask import Flask, render_template, request 
from datetime import datetime
import json
from web3 import Web3, HTTPProvider
import os
import datetime

app = Flask(__name__)


global details, user


def readDetails(contract_type):
    global details
    details = ""
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Auction.json' 
    deployed_contract_address = '0x4051f49c482DD5e801E2A63611a9607CdC45616D' #hash address to access counter feit contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'adduser':
        details = contract.functions.getUsers().call()
    if contract_type == 'product':
        details = contract.functions.getproduct().call()
    if contract_type == 'history':
        details = contract.functions.gethistory().call()
    if contract_type == 'transaction':
        details = contract.functions.gettransaction().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]

    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Auction.json' 
    deployed_contract_address = '0x4051f49c482DD5e801E2A63611a9607CdC45616D' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'adduser':
        details+=currentData
        msg = contract.functions.addUsers(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'product':
        details+=currentData
        msg = contract.functions.addproduct(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'history':
        details+=currentData
        msg = contract.functions.addhistory(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'transaction':
        details+=currentData
        msg = contract.functions.addtransaction(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)


@app.route('/AddBidderAction', methods=['POST'])
def AddBidderAction():
    if request.method == 'POST':

        name = request.form['t1']
        username = request.form['t2']
        password = request.form['t3']
        address = request.form['t4']
        number = request.form['t5']
        email = request.form['t6']

        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Bidder' and array[2] == username:
                status = username + " Username already exists"
                return render_template('BidderSignup.html', data=status)
                break

        if status == "none":
            data = 'Bidder'+"#"+name+"#"+username+"#"+password+"#"+address+"#"+number+"#"+email+"\n"
            saveDataBlockChain(data,"adduser")
            context = 'Details Saved in blockchain'
            return render_template("BidderSignup.html", data=context)
        else:
            context = 'Error in the signup process.'
            return render_template("BidderSignup.html", data=context)


@app.route('/AddSellerAction', methods=['POST'])
def AddSellerAction():
    if request.method == 'POST':

        name = request.form['t1']
        username = request.form['t2']
        password = request.form['t3']
        address = request.form['t4']
        number = request.form['t5']
        email = request.form['t6']

        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Seller' and array[2] == username:
                status = username + " Username already exists"
                return render_template('SellerSignup.html', data=status)
                break

        if status == "none":
            data = 'Seller'+"#"+name+"#"+username+"#"+password+"#"+address+"#"+number+"#"+email+"\n"
            saveDataBlockChain(data,"adduser")
            context = 'Details Saved in blockchain'
            return render_template("SellerSignup.html", data=context)
        else:
            context = 'Error in the signup process.'
            return render_template("SellerSignup.html", data=context)


@app.route('/BidderLoginAction', methods=['POST'])
def BidderLoginAction():
    if request.method == 'POST':
        global bidder_name
        username = request.form['t1']
        password = request.form['t2']
        bidder_name = username
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Bidder' and array[2] == username and array[3] == password:
                status = 'success'
                break

        if status == 'success':
            context = username + ' Welcome.'
            return render_template('BidderScreen.html', data=context)
        else:
            context = 'Invalid Details'
            return render_template('BidderLogin.html', data=context)


@app.route('/SellerLoginAction', methods=['POST'])
def SellerLoginAction():
    if request.method == 'POST':
        global Seller_name
        username = request.form['t1']
        password = request.form['t2']
        Seller_name = username
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Seller' and array[2] == username and array[3] == password:
                status = 'success'
                break

        if status == 'success':
            context = username + ' Welcome.'
            return render_template('SellerScreen.html', data=context)
        else:
            context = 'Invalid Details'
            return render_template('SellerLogin.html', data=context)


@app.route('/AdminLogin',methods=['POST'])
def AdminLogin():
    if request.method == 'POST':
        username = request.form['t1']
        password = request.form['t2']

        if username == 'admin' and password == 'admin':
            context = 'Welcome admin'
            return render_template('AdminScreen.html',data=context)
        else:
            context = 'Invalid Login Details'
            return render_template('AdminLogin.html',data=context)

@app.route('/AddProduct',methods=['POST'])
def AddProduct():
    global Seller_name
    if request.method == 'POST':
        pid = request.form['t1']
        pname = request.form['t2']
        pinfo = request.form['t3']
        price = request.form['t4']
        file = request.files['t5']
    
        filename = file.filename
        print("@@ Input posted = ", filename)
        file_path = os.path.join('static/files/', filename)
        file.save(file_path)
        status = "none"
        readDetails('product')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            if array[0] == pid:
                status = 'Product Already Exists.'
                return render_template('AddProduct.html', data=status)
                break
        
        if status == 'none':
            data = pid+"#"+pname+"#"+pinfo+"#"+price+"#"+filename+"#"+Seller_name+"\n"
            saveDataBlockChain(data,"product")
            context = 'Product Details are added to blockchain.'
            return render_template('AddProduct.html',data=context)

def status(pid,pname,name):
    readDetails('history')
    arr = details.split("\n")
    for i in range(len(arr)-1):
        if array[0] == pid and array[1] == pname and array[3] == name:
            return True
            break
    return False


@app.route('/ViewProduct', methods=['GET', 'POST'])
def ViewProduct():
    if request.method == 'GET':
        global bidder_name,pid,pname,filename
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Product ID','Product Name','Product Information','Product Price','Photo','Place the bid here']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('product')
        arr = details.split("\n")

        for i in range(len(arr) - 1):
            array = arr[i].split("#")

            output += '<tr>'
            for cell in array[0:4]:
                output += f'<td>{font}{cell}{font}</td>'
            download_link = f'<td><img src="static/files/{array[4]}" alt="Image"></td></td>'
            action_cell = f'<td><a href="/Submitbid?pid={array[0]}&pname={array[1]}&filename={array[4]}">{font}Click Here to submit{font}</a></td>' if not status(array[0], array[1], bidder_name) else f'<td>{font}Already Submitted{font}</td>'

            output += download_link + action_cell
            output += '</tr>'

        output += '</table><br/><br/><br/>'

        return render_template('ViewProduct.html', data=output)

@app.route('/Submitbid', methods=['GET', 'POST'])
def Submitbid():
    global bidder_name,pid,pname,filename

    if request.method == 'GET':
        pid = request.args.get('pid')
        pname =  request.args.get('pname')
        filename = request.args.get('filename')
        return render_template('Submitbid.html')

    if request.method == 'POST':
        amount = request.form['t1']
        
        data = pid+"#"+pname+"#"+filename+"#"+bidder_name+"#"+amount+"\n"
        saveDataBlockChain(data, "history")

        context = "Bid Place Successfully."

        return render_template('Submitbid.html', data=context)


def getproductid(name):
    product_id = []
    readDetails('product')
    arr = details.split("\n")
    for i in range(len(arr)-1):
        array = arr[i].split("#")
        if array[5] == name:
            product_id.append(array[0])

    return product_id

def getname():
    name = []
    readDetails('history')
    arr = details.split("\n")
    for i in range(len(arr)-1):
        array = arr[i].split("#")
        name.append(array[3])

    return name      

@app.route('/ViewBid', methods=['GET','POST'])
def ViewBid():
    
    if request.method == 'GET':
        global Seller_name
        product_id = getproductid(Seller_name)
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Product ID','Product Name','Photo','Bidder Name','Amount Bidded']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('history')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] in product_id:
                output += "<tr><td>"+font+array[0]+"</td>"
                output += "<td>"+font+array[1]+"</td>"
                output += f'<td><img src="static/files/{array[2]}" alt="Image"></td></td>'
                output += "<td>"+font+array[3]+"</td>"
                output += "<td>"+font+array[4]+"</td>"
                output += '</tr>'

        output += '</table><br/><br/><br/>'

        return render_template('ViewBid.html', data=output)

@app.route('/Sell', methods=['GET'])
def Sellss():
    global Seller_name
    pid = getproductid(Seller_name)
    name = getname()
    return render_template('Sell.html', pid_all=pid,name_all=name)

@app.route('/Sell', methods=['POST'])
def Sell():
    global student_name
    productid = request.form['pid']
    name = request.form['name']

    data = productid+"#"+name+"\n"
    saveDataBlockChain(data, 'transaction')

    context = 'Product Sold'

    return render_template('Sell.html',data=context)

@app.route('/Result', methods=['GET','POST'])
def Result():
    
    if request.method == 'GET':
        global bidder_name
        
        output = '<table border=1 align=center width=40%>'
        font = '<font size="" color="black">'
        arr = ['Product ID You Won in Auction']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('transaction')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] == bidder_name:
                output += "<tr><td>"+font+array[0]+"</td>"
                output += '</tr>'

        output += '</table><br/><br/><br/>'

        return render_template('Result.html', data=output)

@app.route('/ViewSeller', methods=['GET', 'POST'])
def ViewSeller():
    if request.method == 'GET':
        global bidder_name,pid,pname,filename
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Name','Username','Password','Address','Number','Email']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr) - 1):
            array = arr[i].split("#")
            if array[0] == 'Seller':
                output += '<tr>'
                for cell in array[1:7]:
                    output += f'<td>{font}{cell}{font}</td>'

            output += '</tr>'

        output += '</table><br/><br/><br/>'

        return render_template('ViewSeller.html', data=output)

@app.route('/ViewBidder', methods=['GET', 'POST'])
def ViewBidder():
    if request.method == 'GET':
        global bidder_name,pid,pname,filename
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Name','Username','Password','Address','Number','Email']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr) - 1):
            array = arr[i].split("#")
            if array[0] == 'Bidder':
                output += '<tr>'
                for cell in array[1:7]:
                    output += f'<td>{font}{cell}{font}</td>'

            output += '</tr>'

        output += '</table><br/><br/><br/>'

        return render_template('ViewBidder.html', data=output)

@app.route('/ViewTransaction', methods=['GET', 'POST'])
def ViewTransaction():
    if request.method == 'GET':
        global bidder_name,pid,pname,filename
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Product ID','Bidder who won']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('transaction')
        arr = details.split("\n")

        for i in range(len(arr) - 1):
            array = arr[i].split("#")
            output += '<tr>'
            for cell in array[0:2]:
                output += f'<td>{font}{cell}{font}</td>'

            output += '</tr>'

        output += '</table><br/><br/><br/>'

        return render_template('ViewTransaction.html', data=output)

@app.route('/SellerLogin', methods=['GET', 'POST'])
def SellerLogin():
    if request.method == 'GET':
       return render_template('SellerLogin.html', msg='')

@app.route('/SellerScreen', methods=['GET', 'POST'])
def SellerScreen():
    if request.method == 'GET':
       return render_template('SellerScreen.html', msg='')

@app.route('/SellerSignup', methods=['GET', 'POST'])
def SellerSignup():
    if request.method == 'GET':
       return render_template('SellerSignup.html', msg='')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
       return render_template('index.html', msg='')

@app.route('/ViewTransaction', methods=['GET', 'POST'])
def ViewTransactions():
    if request.method == 'GET':
       return render_template('ViewTransaction.html', msg='')

@app.route('/ViewBidder', methods=['GET', 'POST'])
def ViewBidders():
    if request.method == 'GET':
       return render_template('ViewBidder.html', msg='')

@app.route('/ViewSeller', methods=['GET', 'POST'])
def ViewSellers():
    if request.method == 'GET':
       return render_template('ViewSeller.html', msg='')

@app.route('/Result', methods=['GET', 'POST'])
def Results():
    if request.method == 'GET':
       return render_template('Result.html', msg='')

@app.route('/Sell', methods=['GET', 'POST'])
def Sells():
    if request.method == 'GET':
       return render_template('Sell.html', msg='')

@app.route('/ViewBid', methods=['GET', 'POST'])
def ViewBids():
    if request.method == 'GET':
       return render_template('ViewBid.html', msg='')

@app.route('/Submitbid', methods=['GET', 'POST'])
def Submitbids():
    if request.method == 'GET':
       return render_template('Submitbid.html', msg='')

@app.route('/ViewProduct', methods=['GET', 'POST'])
def ViewProducts():
    if request.method == 'GET':
       return render_template('ViewProduct.html', msg='')

@app.route('/AddProduct', methods=['GET', 'POST'])
def AddProducts():
    if request.method == 'GET':
       return render_template('AddProduct.html', msg='')

@app.route('/AdminLogin', methods=['GET', 'POST'])
def AdminLogins():
    if request.method == 'GET':
       return render_template('AdminLogin.html', msg='')

@app.route('/AdminScreen', methods=['GET', 'POST'])
def AdminScreens():
    if request.method == 'GET':
       return render_template('AdminScreen.html', msg='')

@app.route('/BidderLogin', methods=['GET', 'POST'])
def BidderLogins():
    if request.method == 'GET':
       return render_template('BidderLogin.html', msg='')

@app.route('/BidderScreen', methods=['GET', 'POST'])
def BidderScreens():
    if request.method == 'GET':
       return render_template('BidderScreen.html', msg='')

@app.route('/BidderSignup', methods=['GET', 'POST'])
def BidderSignup():
    if request.method == 'GET':
       return render_template('BidderSignup.html', msg='')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
       return render_template('index.html', msg='')

    
if __name__ == '__main__':
    app.run()       
