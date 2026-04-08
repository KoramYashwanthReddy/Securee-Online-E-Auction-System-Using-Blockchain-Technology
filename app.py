"""from flask import Flask, render_template, request 
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
    blockchain_address = 'http://127.0.0.1:8545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Auction.json' 
    deployed_contract_address = '0xc933421B31A837332CAE5bb7dEfA360479118145' #hash address to access counter feit contract
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
    blockchain_address = 'http://127.0.0.1:8545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Auction.json' 
    deployed_contract_address = '0xc933421B31A837332CAE5bb7dEfA360479118145' #contract address
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
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Bidder' and array[2] == username and array[3] == password:
                status = 'success'
                break

        if status == 'success':
            bidder_name = username
            session.pop('seller', None)
            session.pop('admin', None)
            session.pop('recently_viewed', None)
            session['bidder'] = username
            context = username + ' Welcome.'
            return render_template(
                'BidderScreen.html',
                data=context,
                bidder_analytics=_build_bidder_analytics(username),
                recently_viewed_products=_build_recently_viewed_products(),
                trending_products=_build_trending_auctions()
            )
        else:
            context = 'Invalid Details'
            return render_template('BidderLogin.html', data=context)


@app.route('/SellerLoginAction', methods=['POST'])
def SellerLoginAction():
    if request.method == 'POST':
        global Seller_name
        username = request.form['t1']
        password = request.form['t2']
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Seller' and array[2] == username and array[3] == password:
                status = 'success'
                break

        if status == 'success':
            Seller_name = username
            session.pop('bidder', None)
            session.pop('admin', None)
            session['seller'] = username
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
            session.pop('bidder', None)
            session.pop('seller', None)
            session['admin'] = 'admin'
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
            array = arr[i].split("#")
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
        array = arr[i].split("#")
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
            action_cell = (
                f'<td><button type="button" class="bid-btn" data-pid="{array[0]}" data-pname="{array[1]}" data-filename="{array[4]}">Submit Bid</button></td>'
                if not status(array[0], array[1], bidder_name)
                else f'<td>{font}Already Submitted{font}</td>'
            )

            output += download_link + action_cell
            output += '</tr>'

        output += '</table><br/><br/><br/>'

        return render_template('ViewProduct.html', data=output)

@app.route('/Submitbid', methods=['GET', 'POST'])
def Submitbid():
    global bidder_name,pid,pname,filename

    if request.method == 'GET':
        return redirect(url_for('ViewProduct'))

    if request.method == 'POST':
        amount = request.form['t1']
        
        data = pid+"#"+pname+"#"+filename+"#"+bidder_name+"#"+amount+"\n"
        saveDataBlockChain(data, "history")

        context = "Bid Place Successfully."

        return redirect(url_for('ViewProduct', bid_notice='success'))


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
"""







































# from flask import Flask, render_template, request, session
# from datetime import datetime
# import json
# from web3 import Web3, HTTPProvider
# import os
# import datetime

# app = Flask(__name__)
# app.secret_key = "super_secret_key"

# details = ""

# # ================= BLOCKCHAIN CONNECTION HELPER =================

# def get_contract():
#     try:
#         blockchain_address = 'http://127.0.0.1:8545'
#         web3 = Web3(HTTPProvider(blockchain_address))

#         if not web3.isConnected():
#             print("❌ Blockchain not connected")
#             return None, None

#         web3.eth.defaultAccount = web3.eth.accounts[0]

#         with open('Auction.json') as file:
#             contract_json = json.load(file)
#             contract_abi = contract_json['abi']

#         contract = web3.eth.contract(
#             address='0xc933421B31A837332CAE5bb7dEfA360479118145',
#             abi=contract_abi
#         )

#         return web3, contract

#     except Exception as e:
#         print("❌ Contract Load Error:", str(e))
#         return None, None




















from flask import Flask, render_template, request, session, redirect, url_for
import re
from datetime import datetime
import json
from web3 import Web3
from web3.providers.rpc import HTTPProvider
import os
import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)   # more secure than static key

details = ""

# ================= BLOCKCHAIN CONNECTION HELPER =================

def get_contract():
    try:
        blockchain_address = "http://127.0.0.1:8545"
        web3 = Web3(HTTPProvider(blockchain_address))

        # Web3 v6 connection check
        if not web3.is_connected():
            print("❌ Blockchain not connected")
            return None, None

        # set default account
        web3.eth.default_account = web3.eth.accounts[0]

        # load contract ABI
        with open("Auction.json", "r") as file:
            contract_json = json.load(file)
            contract_abi = contract_json["abi"]

        contract = web3.eth.contract(
            address="0xc933421B31A837332CAE5bb7dEfA360479118145",
            abi=contract_abi
        )

        return web3, contract

    except Exception as e:
        print("❌ Contract Load Error:", str(e))
        return None, None

# ================= READ DATA FROM BLOCKCHAIN =================

def readDetails(contract_type):

    web3, contract = get_contract()

    if contract is None:
        print("⚠ Contract not available")
        return ""

    try:
        # Map contract types to smart contract functions
        contract_functions = {
            "adduser": contract.functions.getUsers,
            "product": contract.functions.getproduct,
            "history": contract.functions.gethistory,
            "transaction": contract.functions.gettransaction
        }

        func = contract_functions.get(contract_type)

        if not func:
            print(f"⚠ Invalid contract type: {contract_type}")
            return ""

        # Call smart contract
        result = func().call()

        if result is None:
            return ""

        # Convert to string if blockchain returns bytes
        if isinstance(result, bytes):
            result = result.decode("utf-8")

        result = str(result)

        # Remove default prefix
        if result.startswith("empty"):
            result = result.replace("empty", "", 1)

        return result

    except Exception as e:
        print(f"❌ Blockchain Read Error ({contract_type}):", e)
        return ""

# ================= SAVE DATA TO BLOCKCHAIN =================
def saveDataBlockChain(currentData, contract_type):
    global details

    web3, contract = get_contract()

    if contract is None:
        return False

    try:
        # Read existing data first
        existing_data = readDetails(contract_type)

        if existing_data:
            details = existing_data + currentData
        else:
            details = currentData

        if contract_type == 'adduser':
            tx_hash = contract.functions.addUsers(details).transact()

        elif contract_type == 'product':
            tx_hash = contract.functions.addproduct(details).transact()

        elif contract_type == 'history':
            tx_hash = contract.functions.addhistory(details).transact()

        elif contract_type == 'transaction':
            tx_hash = contract.functions.addtransaction(details).transact()

        else:
            print("⚠ Invalid contract type in saveDataBlockChain")
            return False

        # ✅ FIXED HERE
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        if contract_type == 'history':
            _record_bid_timestamp(currentData, receipt, web3)

        print("✅ Blockchain transaction successful:", receipt.transactionHash.hex())
        return True

    except Exception as e:
        print("❌ Blockchain Save Error:", str(e))
        return False


# ================= AUCTION HELPERS =================

MIN_BID_INCREMENT = 10
AUCTION_DURATION_HOURS = 1
HISTORY_META_FILE = os.path.join("static", "files", "bid_history_meta.json")
AUCTION_EXTENSION_FILE = os.path.join("static", "files", "auction_extensions.json")
WATCHLIST_FILE = os.path.join("static", "files", "watchlist.json")
PAYMENT_FILE = os.path.join("static", "files", "payments.json")
NOTIFICATION_FILE = os.path.join("static", "files", "notifications.json")
AUCTION_EXTENSION_WINDOW_SECONDS = 120
AUCTION_EXTENSION_SECONDS = 120
VIEW_PRODUCT_PAGE_SIZE = 10


def _safe_int(value, default=0):
    try:
        return int(str(value).strip())
    except Exception:
        return default


def _parse_datetime(value):
    if not value:
        return None

    value = str(value).strip()
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M",
    ]

    for fmt in formats:
        try:
            return datetime.datetime.strptime(value, fmt)
        except Exception:
            continue

    return None


def _split_rows(raw_data):
    if not raw_data:
        return []

    rows = []
    for row in str(raw_data).split("\n"):
        if row.strip():
            rows.append(row.split("#"))
    return rows


def _ensure_parent_dir(file_path):
    parent_dir = os.path.dirname(file_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)


def _load_history_meta():
    try:
        if not os.path.exists(HISTORY_META_FILE):
            return {}
        with open(HISTORY_META_FILE, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_history_meta(meta):
    try:
        _ensure_parent_dir(HISTORY_META_FILE)
        with open(HISTORY_META_FILE, "w", encoding="utf-8") as handle:
            json.dump(meta, handle, indent=2)
    except Exception as exc:
        print("⚠ Could not save bid history meta:", exc)


def _load_json_file(file_path):
    try:
        if not os.path.exists(file_path):
            return {}
        with open(file_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_json_file(file_path, payload):
    try:
        _ensure_parent_dir(file_path)
        with open(file_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        return True
    except Exception as exc:
        print("⚠ Could not save JSON file:", exc)
        return False


def _load_auction_extensions():
    return _load_json_file(AUCTION_EXTENSION_FILE)


def _save_auction_extensions(payload):
    return _save_json_file(AUCTION_EXTENSION_FILE, payload)


def _get_auction_extension_seconds(pid):
    meta = _load_auction_extensions()
    try:
        return int(meta.get(pid, 0))
    except Exception:
        return 0


def _extend_auction_for_bid(pid, extra_seconds=AUCTION_EXTENSION_SECONDS):
    meta = _load_auction_extensions()
    current = _safe_int(meta.get(pid, 0))
    meta[pid] = current + max(0, _safe_int(extra_seconds, AUCTION_EXTENSION_SECONDS))
    _save_auction_extensions(meta)
    return meta[pid]


def _load_watchlist():
    return _load_json_file(WATCHLIST_FILE)


def _save_watchlist(payload):
    return _save_json_file(WATCHLIST_FILE, payload)


def _get_watchlist_for_user(username):
    watchlist = _load_watchlist()
    items = watchlist.get(username, [])
    if not isinstance(items, list):
        return []
    return [str(pid) for pid in items if str(pid).strip()]


def _add_watchlist_item(username, pid):
    watchlist = _load_watchlist()
    items = watchlist.get(username, [])
    if not isinstance(items, list):
        items = []
    items = [str(item) for item in items if str(item).strip()]
    if pid not in items:
        items.append(pid)
    watchlist[username] = items
    _save_watchlist(watchlist)
    return items


def _track_recently_viewed_product(pid):
    viewed = session.get("recently_viewed", [])
    if not isinstance(viewed, list):
        viewed = []

    pid = str(pid).strip()
    if not pid:
        return viewed

    viewed = [item for item in viewed if item != pid]
    viewed.insert(0, pid)
    session["recently_viewed"] = viewed[:5]
    session.modified = True
    return session["recently_viewed"]


def _get_recently_viewed_ids():
    viewed = session.get("recently_viewed", [])
    if not isinstance(viewed, list):
        return []
    cleaned = []
    for pid in viewed:
        pid = str(pid).strip()
        if pid and pid not in cleaned:
            cleaned.append(pid)
    return cleaned[:5]


def _build_recently_viewed_products():
    product_lookup = _get_product_lookup()
    products = []
    now = datetime.datetime.now()

    for pid in _get_recently_viewed_ids():
        product = product_lookup.get(pid)
        if not product:
            continue

        snapshot = _get_bid_snapshot(pid)
        auction_end = snapshot["auction_end"] if snapshot else _auction_end_from_product(product)
        products.append({
            "pid": pid,
            "pname": product["pname"],
            "pinfo": product["pinfo"],
            "base_price": product["base_price"],
            "highest_bid": snapshot["highest_bid"] if snapshot else product["base_price"],
            "filename": product["filename"],
            "status": _auction_status(auction_end, now),
            "remaining": _format_remaining_time(auction_end, now),
        })

    return products


def _build_bidder_analytics(username):
    history_rows = _split_rows(readDetails("history"))
    transaction_rows = _get_transaction_rows()

    total_bids = sum(1 for row in history_rows if len(row) >= 4 and row[3] == username)
    participated = []
    for row in history_rows:
        if len(row) >= 4 and row[3] == username and row[0] not in participated:
            participated.append(row[0])

    won = []
    for row in transaction_rows:
        if len(row) >= 2 and row[1] == username and row[0] not in won:
            won.append(row[0])

    win_rate = round((len(won) / len(participated)) * 100, 2) if participated else 0

    return {
        "username": username,
        "total_bids": total_bids,
        "auctions_participated": len(participated),
        "auctions_won": len(won),
        "win_rate": win_rate,
        "recently_viewed": len(_get_recently_viewed_ids()),
    }


def _build_trending_auctions():
    product_lookup = _get_product_lookup()
    history_rows = _split_rows(readDetails("history"))
    now = datetime.datetime.now()
    stats = {}

    for row in history_rows:
        if len(row) < 5:
            continue
        pid = row[0]
        amount = _safe_int(row[4])
        bidder = row[3]
        item = stats.setdefault(pid, {
            "pid": pid,
            "bid_count": 0,
            "highest_bid": 0,
            "bid_increase": 0,
            "leader": bidder,
        })
        product = product_lookup.get(pid)
        base_price = product["base_price"] if product else 0
        item["bid_count"] += 1
        if amount > item["highest_bid"]:
            item["highest_bid"] = amount
            item["leader"] = bidder
        item["bid_increase"] = max(item["bid_increase"], max(0, amount - base_price))

    trending = []
    for pid, item in stats.items():
        product = product_lookup.get(pid)
        if not product:
            continue
        auction_end = _auction_end_from_product(product)
        trending.append({
            "pid": pid,
            "pname": product["pname"],
            "base_price": product["base_price"],
            "highest_bid": item["highest_bid"] or product["base_price"],
            "bid_count": item["bid_count"],
            "bid_increase": item["bid_increase"],
            "leader": item["leader"],
            "filename": product["filename"],
            "time_left": _format_remaining_time(auction_end, now),
        })

    trending.sort(key=lambda item: (item["bid_count"], item["bid_increase"], item["highest_bid"]), reverse=True)
    return trending[:5]


def _auction_end_from_product(product):
    auction_start = _parse_datetime(product.get("creation_time"))
    if not auction_start:
        return None
    extension_seconds = _get_auction_extension_seconds(product["pid"])
    return auction_start + datetime.timedelta(
        hours=AUCTION_DURATION_HOURS,
        seconds=extension_seconds
    )


def _auction_progress_percent(product, auction_end, now=None):
    now = now or datetime.datetime.now()
    auction_start = _parse_datetime(product.get("creation_time"))
    if not auction_start or not auction_end:
        return 0
    total_seconds = max(1, int((auction_end - auction_start).total_seconds()))
    elapsed_seconds = max(0, int((now - auction_start).total_seconds()))
    return max(0, min(100, int((elapsed_seconds / total_seconds) * 100)))


def _format_remaining_time(auction_end, now=None):
    now = now or datetime.datetime.now()
    if not auction_end:
        return "Unavailable"
    remaining = int((auction_end - now).total_seconds())
    if remaining <= 0:
        return "Closed"
    minutes, seconds = divmod(remaining, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m {seconds}s"


def _latest_user_record(username):
    latest = None
    for row in _get_user_records():
        if len(row) >= 7 and row[2] == username:
            latest = row
    return latest


def _build_user_payload(row):
    if not row or len(row) < 7:
        return None
    return {
        "role": row[0],
        "name": row[1],
        "username": row[2],
        "password": row[3],
        "address": row[4],
        "phone": row[5],
        "email": row[6],
    }


def _generate_transaction_id():
    return f"TXN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{os.urandom(3).hex().upper()}"


def _load_payments():
    return _load_json_file(PAYMENT_FILE)


def _save_payments(payload):
    return _save_json_file(PAYMENT_FILE, payload)


def _load_notifications():
    return _load_json_file(NOTIFICATION_FILE)


def _save_notifications(payload):
    return _save_json_file(NOTIFICATION_FILE, payload)


def _append_notification(recipient, notification):
    data = _load_notifications()
    items = data.get(recipient, [])
    if not isinstance(items, list):
        items = []
    items.append(notification)
    data[recipient] = items
    _save_notifications(data)


def _broadcast_notification(recipients, notification):
    for recipient in recipients:
        _append_notification(recipient, dict(notification))


def _get_notification_items(username):
    data = _load_notifications()
    items = data.get(username, [])
    if not isinstance(items, list):
        return []
    return items


def _mark_notifications_read(username, ids=None):
    data = _load_notifications()
    items = data.get(username, [])
    if not isinstance(items, list):
        return []

    id_set = set(ids or [])
    updated = []
    for item in items:
        if not isinstance(item, dict):
            continue
        if not id_set or item.get("id") in id_set:
            item["read"] = True
        updated.append(item)
    data[username] = updated
    _save_notifications(data)
    return updated


def _payment_records_list():
    data = _load_payments()
    if isinstance(data, dict):
        return list(data.values())
    if isinstance(data, list):
        return data
    return []


def _payment_for_product(pid, username=None):
    for record in _payment_records_list():
        if record.get("product_id") == pid and (username is None or record.get("username") == username):
            return record
    return None


def _suspicious_bid_analysis():
    history_rows = _get_history_rows_with_meta()
    by_user = {}
    suspicious_records = []
    suspicious_users = set()

    for row in history_rows:
        username = row.get("bidder")
        pid = row.get("pid")
        if not username or not pid:
            continue
        by_user.setdefault(username, []).append(row)

    for username, rows in by_user.items():
        rows = sorted(rows, key=lambda item: item.get("time") or "")
        for index, row in enumerate(rows):
            previous = rows[index - 1] if index > 0 else None
            if previous and row.get("time") and previous.get("time"):
                current_dt = _parse_datetime(row["time"])
                previous_dt = _parse_datetime(previous["time"])
                if current_dt and previous_dt:
                    seconds_gap = abs((current_dt - previous_dt).total_seconds())
                    if seconds_gap <= 60:
                        suspicious_users.add(username)
                        suspicious_records.append({
                            "username": username,
                            "pid": row.get("pid"),
                            "reason": "Multiple bids within 60 seconds",
                            "time": row.get("time"),
                            "amount": row.get("amount"),
                        })
            same_pid_recent = [
                item for item in rows
                if item.get("pid") == row.get("pid") and item.get("time")
            ]
            if len(same_pid_recent) >= 3:
                times = [_parse_datetime(item["time"]) for item in same_pid_recent[-3:]]
                if all(times) and (max(times) - min(times)).total_seconds() <= 300:
                    suspicious_users.add(username)
                    suspicious_records.append({
                        "username": username,
                        "pid": row.get("pid"),
                        "reason": "Rapid repeated bidding on same product",
                        "time": row.get("time"),
                        "amount": row.get("amount"),
                    })

    product_lookup = _get_product_lookup()
    for username, rows in by_user.items():
        for index, row in enumerate(rows):
            previous = rows[index - 1] if index > 0 else None
            if previous:
                prev_amount = _safe_int(previous.get("amount"), 0)
                curr_amount = _safe_int(row.get("amount"), 0)
                if prev_amount and curr_amount >= int(prev_amount * 1.75):
                    suspicious_users.add(username)
                    suspicious_records.append({
                        "username": username,
                        "pid": row.get("pid"),
                        "reason": f"Unusually large jump from ₹{prev_amount} to ₹{curr_amount}",
                        "time": row.get("time"),
                        "amount": curr_amount,
                    })

    return {
        "users": sorted(suspicious_users),
        "records": suspicious_records,
        "products": product_lookup,
    }


def _record_bid_timestamp(current_data, receipt, web3):
    try:
        block = web3.eth.get_block(receipt.blockNumber)
        block_time = datetime.datetime.fromtimestamp(block.timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        block_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    meta = _load_history_meta()
    for row in str(current_data).split("\n"):
        if row.strip():
            meta[row.strip()] = block_time
    _save_history_meta(meta)


def _auction_status(auction_end, now=None):
    now = now or datetime.datetime.now()
    if not auction_end:
        return "unknown"
    if now >= auction_end:
        return "closed"
    if (auction_end - now).total_seconds() <= 300:
        return "ending-soon"
    return "active"


def _format_currency(value):
    return f"₹{int(value)}"


def _infer_category(pname, pinfo):
    text = f"{pinfo} {pname}".strip().lower()
    if not text:
        return "Other"

    category_map = [
        ("electronics", ["phone", "mobile", "laptop", "computer", "camera", "tv", "tablet"]),
        ("fashion", ["shirt", "dress", "shoe", "watch", "jewelry", "jewel", "cloth", "bag"]),
        ("vehicles", ["car", "bike", "motor", "truck", "scooter", "bus"]),
        ("real estate", ["house", "flat", "plot", "land", "villa", "apartment"]),
        ("art & antiques", ["vintage", "antique", "painting", "sculpture", "collectible"]),
        ("sports", ["bat", "ball", "racket", "cricket", "football", "shuttlecock"]),
        ("agriculture", ["mango", "fruit", "vegetable", "grain", "farm"]),
    ]

    for category, keywords in category_map:
        if any(keyword in text for keyword in keywords):
            return category.title()

    return pinfo.split("|")[0].split(",")[0].split(";")[0].split(":")[0].split("-")[0].strip().title() or "Other"


def _get_product_lookup():
    product_lookup = {}

    for row in _split_rows(readDetails("product")):
        if len(row) < 6:
            continue

        creation_time = row[6] if len(row) >= 7 else ""
        product_lookup[row[0]] = {
            "pid": row[0],
            "pname": row[1],
            "pinfo": row[2],
            "base_price": _safe_int(row[3]),
            "filename": row[4],
            "seller": row[5],
            "creation_time": creation_time,
        }

    return product_lookup


def _get_bid_snapshot(pid):
    product_lookup = _get_product_lookup()
    product = product_lookup.get(pid)

    if not product:
        return None

    highest_bid = product["base_price"]
    leader = ""
    bidders = set()

    for row in _split_rows(readDetails("history")):
        if len(row) < 5 or row[0] != pid:
            continue

        amount = _safe_int(row[4], product["base_price"])
        bidder = row[3]
        bidders.add(bidder)

        if amount > highest_bid:
            highest_bid = amount
            leader = bidder

    auction_start = _parse_datetime(product["creation_time"])
    auction_end = _auction_end_from_product(product)

    return {
        "product": product,
        "highest_bid": highest_bid,
        "leader": leader,
        "bidder_count": len(bidders),
        "auction_end": auction_end,
        "auction_start": auction_start,
    }


def build_seller_dashboard(seller_name):
    product_lookup = _get_product_lookup()
    history_rows = _split_rows(readDetails("history"))
    transaction_rows = _split_rows(readDetails("transaction"))

    seller_products = {
        pid: data for pid, data in product_lookup.items() if data["seller"] == seller_name
    }

    highest_by_pid = {}
    sold_products = []
    sold_pid_tracker = set()
    total_earnings = 0

    for row in history_rows:
        if len(row) < 5:
            continue

        pid = row[0]
        if pid not in seller_products:
            continue

        amount = _safe_int(row[4], seller_products[pid]["base_price"])
        if pid not in highest_by_pid or amount > highest_by_pid[pid]:
            highest_by_pid[pid] = amount

    for row in transaction_rows:
        if len(row) < 2:
            continue

        pid = row[0]
        if pid not in seller_products or pid in sold_pid_tracker:
            continue

        sold_pid_tracker.add(pid)

        winning_amount = highest_by_pid.get(pid, seller_products[pid]["base_price"])
        total_earnings += winning_amount
        sold_products.append(
            {
                "pid": pid,
                "product_name": seller_products[pid]["pname"],
                "winner": row[1],
                "winning_bid": winning_amount,
            }
        )

    sold_products.sort(key=lambda item: item["winning_bid"], reverse=True)

    total_products_listed = len(seller_products)
    average_bid_per_product = 0
    if total_products_listed:
        average_bid_per_product = int(
            sum(highest_by_pid.get(pid, seller_products[pid]["base_price"]) for pid in seller_products) / total_products_listed
        )

    return {
        "seller_name": seller_name,
        "total_products_listed": total_products_listed,
        "total_products_sold": len(sold_products),
        "total_earnings": total_earnings,
        "highest_selling_product": max(sold_products, key=lambda item: item["winning_bid"]) if sold_products else None,
        "average_bid_per_product": average_bid_per_product,
        "sold_products": sold_products,
    }


def build_seller_analytics(seller_name):
    dashboard = build_seller_dashboard(seller_name)
    highest_product = dashboard["highest_selling_product"]
    return {
        "seller_name": seller_name,
        "total_products_listed": dashboard["total_products_listed"],
        "total_products_sold": dashboard["total_products_sold"],
        "total_earnings": dashboard["total_earnings"],
        "highest_selling_product": highest_product["product_name"] if highest_product else "N/A",
        "highest_selling_amount": highest_product["winning_bid"] if highest_product else 0,
        "average_bid_per_product": dashboard["average_bid_per_product"],
    }


def _render_view_product_page():
    bidder_name = session.get('bidder')

    if not bidder_name:
        return render_template('BidderLogin.html', data="⚠ Please login first")

    product_lookup = _get_product_lookup()
    history_rows = _split_rows(readDetails('history'))
    now = datetime.datetime.now()
    suspicious_bundle = _suspicious_bid_analysis()
    suspicious_users = set(suspicious_bundle["users"])
    watchlist_ids = set(_get_watchlist_for_user(bidder_name))
    page = max(1, _safe_int(request.args.get("page", 1), 1))
    product_items = list(product_lookup.items())
    total_products = len(product_items)
    total_pages = max(1, (total_products + VIEW_PRODUCT_PAGE_SIZE - 1) // VIEW_PRODUCT_PAGE_SIZE)
    page = min(page, total_pages)
    start_index = (page - 1) * VIEW_PRODUCT_PAGE_SIZE
    end_index = start_index + VIEW_PRODUCT_PAGE_SIZE
    paginated_items = product_items[start_index:end_index]

    output = (
        '<table class="table table-striped auction-product-table" id="auctionProductTable">'
        '<thead><tr>'
        '<th>Product ID</th>'
        '<th>Product Name</th>'
        '<th>Category</th>'
        '<th>Product Information</th>'
        '<th>Base Price</th>'
        '<th>Highest Bid</th>'
        '<th>Leading Bidder</th>'
        '<th>Bidders</th>'
        '<th>Photo</th>'
        '<th>Auction End Time</th>'
        '<th>Progress</th>'
        '<th>Status</th>'
        '<th>Countdown</th>'
        '<th>Chart</th>'
        '<th>Watchlist</th>'
        '<th>Action</th>'
        '</tr></thead><tbody>'
    )

    if not product_lookup:
        output += (
            '<tr class="table-empty-row" data-placeholder="true"><td colspan="16" style="text-align:center;">'
            'No active products found'
            '</td></tr>'
        )

    for pid, product in paginated_items:
        pname = product['pname']
        pinfo = product['pinfo']
        base_price = product['base_price']
        filename = product['filename']
        creation_time = product['creation_time']

        highest_bid = base_price
        leading_user = ""
        bidders = set()

        for harray in history_rows:
            if len(harray) < 5 or harray[0] != pid:
                continue

            amount = _safe_int(harray[4], base_price)
            user = harray[3]
            bidders.add(user)

            if amount > highest_bid:
                highest_bid = amount
                leading_user = user

        bidder_count = len(bidders)
        auction_start = _parse_datetime(creation_time)
        auction_end = _auction_end_from_product(product)
        auction_end_display = (
            auction_end.strftime("%d-%m-%Y %I:%M %p") if auction_end else "Unavailable"
        )
        auction_end_attr = (
            auction_end.strftime("%Y-%m-%d %H:%M:%S") if auction_end else ""
        )
        auction_state = _auction_status(auction_end, now)
        auction_closed = auction_state == "closed"
        ending_soon = auction_state == "ending-soon"
        auction_end_ts = int(auction_end.timestamp()) if auction_end else 0
        row_classes = []
        if leading_user and leading_user == bidder_name:
            row_classes.append("auction-row-leading")
        if leading_user in suspicious_users:
            row_classes.append("auction-row-suspicious")
        row_class_attr = f' class="{" ".join(row_classes)}"' if row_classes else ""

        output += (
            f'<tr{row_class_attr} data-product-name="{pname.lower()}" '
            f'data-category="{_infer_category(pname, pinfo).lower()}" '
            f'data-base-price="{base_price}" '
            f'data-highest-bid="{highest_bid}" '
            f'data-start-ts="{int(auction_start.timestamp()) if auction_start else 0}" '
            f'data-end-ts="{auction_end_ts}" '
            f'data-status="{auction_state}" '
            f'data-active="{str(not auction_closed).lower()}" '
            f'data-suspicious="{str(leading_user in suspicious_users).lower()}">'
        )
        output += f'<td>{pid}</td>'
        output += f'<td>{pname}</td>'
        output += f'<td>{_infer_category(pname, pinfo)}</td>'
        output += f'<td>{pinfo}</td>'
        output += f'<td>₹{base_price}</td>'
        output += f'<td class="highest-bid" data-pid="{pid}">₹{highest_bid}</td>'

        if leading_user:
            leader_display = leading_user
            if leading_user in suspicious_users:
                leader_display += ' <span class="badge bg-danger">Suspicious</span>'
            output += f'<td class="leader" data-pid="{pid}">{leader_display}</td>'
        else:
            output += f'<td class="leader" data-pid="{pid}">No Bids</td>'

        output += f'<td class="bid-count" data-pid="{pid}">{bidder_count}</td>'
        output += f'<td><img src="/static/files/{filename}" alt="{pname}" width="100"></td>'
        output += f'<td>{auction_end_display}</td>'
        output += (
            '<td>'
            f'<div class="auction-progress-track" data-progress-pid="{pid}">'
            '<div class="auction-progress-fill" style="width:0%"></div>'
            '</div>'
            f'<div class="auction-progress-label" data-progress-label="{pid}">0%</div>'
            '</td>'
        )
        output += (
            '<td>'
            f'<span class="auction-status-badge {"is-ending-soon" if ending_soon else ("is-closed" if auction_closed else "is-live")}">'
            f'{"Closed" if auction_closed else ("Ending Soon" if ending_soon else "Live")}'
            '</span>'
            '</td>'
        )

        if auction_end_attr:
            output += f'<td><span class="timer" data-end="{auction_end_attr}"></span></td>'
        else:
            output += '<td><span class="timer">Unavailable</span></td>'

        output += f'<td><a class="btn btn-sm btn-outline-info" href="/BidChart/{pid}">View Chart</a></td>'

        if bidder_name:
            watched_class = "is-watched" if pid in watchlist_ids else ""
            watched_label = "Watching" if pid in watchlist_ids else "Add to Watchlist"
            output += (
                '<td>'
                '<form class="watchlist-form" method="post" action="/AddWatchlist">'
                f'<input type="hidden" name="pid" value="{pid}">'
                f'<button type="submit" class="watchlist-btn {watched_class}" '
                f'data-pid="{pid}" data-pname="{pname}">{watched_label}</button>'
                '</form>'
                '</td>'
            )
        else:
            output += '<td><span class="watchlist-hint">Login to watch</span></td>'

        if auction_closed:
            output += '<td><span class="btn btn-sm btn-secondary">Closed</span></td>'
        else:
            output += (
                '<td><div class="product-action-stack">'
                f'<button type="button" class="view-btn" '
                f'data-pid="{pid}" data-pname="{pname}" data-filename="{filename}" '
                f'data-base-price="{base_price}" data-current-highest="{highest_bid}">View</button>'
                f'<button type="button" class="bid-btn" '
                f'data-pid="{pid}" data-pname="{pname}" data-filename="{filename}" '
                f'data-base-price="{base_price}" data-current-highest="{highest_bid}">'
                'Submit Bid</button></div></td>'
            )

        output += '</tr>'

    output += '</tbody></table><br/><br/>'

    if total_pages > 1:
        pagination_bits = ['<div class="view-product-pagination">']
        prev_page = max(1, page - 1)
        next_page = min(total_pages, page + 1)
        pagination_bits.append(f'<a class="page-link-btn" href="/ViewProduct?page={prev_page}">Previous</a>')
        for page_no in range(1, total_pages + 1):
            active_class = ' is-active' if page_no == page else ''
            pagination_bits.append(f'<a class="page-link-btn{active_class}" href="/ViewProduct?page={page_no}">{page_no}</a>')
        pagination_bits.append(f'<a class="page-link-btn" href="/ViewProduct?page={next_page}">Next</a>')
        pagination_bits.append('</div>')
        output += ''.join(pagination_bits)

    return render_template('ViewProduct.html', data=output)


def _process_bid_submission():
    bidder_name = session.get('bidder')

    if not bidder_name:
        return render_template('BidderLogin.html', data="⚠ Please login first")

    if request.method == 'GET':
        return redirect(url_for('ViewProduct'))

    pid = request.form.get('pid', '').strip()
    pname = request.form.get('pname', '').strip()
    filename = request.form.get('filename', '').strip()
    amount_text = request.form.get('t1', '').strip()

    if not pid or not pname or not filename or not amount_text.isdigit():
        return redirect(url_for('ViewProduct', bid_notice='invalid'))

    snapshot = _get_bid_snapshot(pid)

    if not snapshot:
        return redirect(url_for('ViewProduct', bid_notice='invalid'))

    product = snapshot['product']
    highest_bid = snapshot['highest_bid']
    base_price = product['base_price']
    auction_end = snapshot['auction_end']
    previous_leader = snapshot['leader']
    amount = _safe_int(amount_text)

    if product['pname'] != pname or product['filename'] != filename:
        return redirect(url_for('ViewProduct', bid_notice='invalid'))

    if auction_end and datetime.datetime.now() >= auction_end:
        return redirect(url_for('ViewProduct', bid_notice='closed'))

    if auction_end:
        seconds_left = int((auction_end - datetime.datetime.now()).total_seconds())
        if 0 < seconds_left <= AUCTION_EXTENSION_WINDOW_SECONDS:
            _extend_auction_for_bid(pid)
            snapshot = _get_bid_snapshot(pid)
            auction_end = snapshot['auction_end'] if snapshot else auction_end

    if amount <= base_price:
        return redirect(url_for('ViewProduct', bid_notice='low'))

    if amount < highest_bid + MIN_BID_INCREMENT:
        return redirect(url_for('ViewProduct', bid_notice='increment'))

    data = f"{pid}#{pname}#{filename}#{bidder_name}#{amount}\n"
    success = saveDataBlockChain(data, "history")

    if success:
        if previous_leader and previous_leader != bidder_name:
            _append_notification(previous_leader, {
                "id": _generate_transaction_id(),
                "type": "outbid",
                "message": f"You have been outbid on {pname} by {bidder_name}.",
                "link": f"/BidChart/{pid}",
                "read": False,
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "product_id": pid,
            })
        return redirect(url_for('ViewProduct', bid_notice='success'))

    return redirect(url_for('ViewProduct', bid_notice='error'))


def _render_seller_dashboard_page(message=None, dashboard=None):
    seller_name = session.get('seller')

    if not seller_name:
        return render_template('SellerLogin.html', data="⚠ Please login first")

    if dashboard is None:
        dashboard = build_seller_dashboard(seller_name)
    seller_analytics = build_seller_analytics(seller_name)

    return render_template(
        'SellerScreen.html',
        data=message or f"✅ Welcome {seller_name}",
        seller_dashboard=dashboard,
        seller_analytics=seller_analytics
    )


def _get_user_context(role_hint=None):
    if role_hint == "Seller" and session.get('seller'):
        return "Seller", session.get('seller')
    if role_hint == "Bidder" and session.get('bidder'):
        return "Bidder", session.get('bidder')
    if role_hint == "Admin" and session.get('admin'):
        return "Admin", session.get('admin')
    if session.get('seller'):
        return "Seller", session.get('seller')
    if session.get('bidder'):
        return "Bidder", session.get('bidder')
    if session.get('admin'):
        return "Admin", session.get('admin')
    return None, None


def _get_user_records():
    latest = {}
    for row in _split_rows(readDetails("adduser")):
        if len(row) >= 7:
            latest[row[2]] = row
    return list(latest.values())


def _get_transaction_rows():
    return [row for row in _split_rows(readDetails("transaction")) if len(row) >= 2]


def _get_history_rows_with_meta():
    history_rows = []
    meta = _load_history_meta()

    for row in _split_rows(readDetails("history")):
        if len(row) < 5:
            continue

        key = "#".join(row[:5])
        history_rows.append({
            "pid": row[0],
            "pname": row[1],
            "filename": row[2],
            "bidder": row[3],
            "amount": _safe_int(row[4]),
            "time": meta.get(key, ""),
        })

    return history_rows


def _build_admin_analytics():
    user_rows = _get_user_records()
    product_rows = _split_rows(readDetails("product"))
    history_rows = _split_rows(readDetails("history"))
    transaction_rows = _get_transaction_rows()

    return {
        "total_users": len(user_rows),
        "total_products": len([row for row in product_rows if len(row) >= 6]),
        "total_bids": len(history_rows),
        "total_transactions": len(transaction_rows),
    }


def _build_leaderboard():
    history_rows = _split_rows(readDetails("history"))
    leader_counts = {}

    for row in history_rows:
        if len(row) < 4:
            continue

        username = row[3]
        leader_counts[username] = leader_counts.get(username, 0) + 1

    return [
        {"rank": index + 1, "username": username, "total_bids": count}
        for index, (username, count) in enumerate(
            sorted(leader_counts.items(), key=lambda item: item[1], reverse=True)[:10]
        )
    ]


def _build_profile(role_hint=None):
    role, username = _get_user_context(role_hint=role_hint)
    if not username:
        return None

    user_row = _latest_user_record(username)
    history_rows = _split_rows(readDetails("history"))
    transaction_rows = _get_transaction_rows()
    product_rows = _split_rows(readDetails("product"))

    total_bids = sum(1 for row in history_rows if len(row) >= 4 and row[3] == username)
    auctions_won = sum(1 for row in transaction_rows if len(row) >= 2 and row[1] == username)
    products_listed = sum(1 for row in product_rows if len(row) >= 6 and row[5] == username)

    return {
        "username": username,
        "role": role,
        "name": user_row[1] if user_row else username,
        "email": user_row[6] if user_row else "",
        "phone": user_row[5] if user_row else "",
        "address": user_row[4] if user_row else "",
        "total_bids": total_bids,
        "auctions_won": auctions_won,
        "products_listed": products_listed if role == "Seller" else 0,
    }


# ================= ADD BIDDER =================

@app.route('/AddBidderAction', methods=['POST'])
def AddBidderAction():

    name = request.form.get('t1', '').strip()
    username = request.form.get('t2', '').strip()
    password = request.form.get('t3', '').strip()
    address = request.form.get('t4', '').strip()
    number = request.form.get('t5', '').strip()
    email = request.form.get('t6', '').strip()

    # 🔒 Basic Validation
    if not all([name, username, password, address, number, email]):
        return render_template(
            'BidderSignup.html',
            data="⚠ All fields are required"
        )

    # 🔎 Read existing users
    existing_data = readDetails('adduser')

    if existing_data:
        for row in existing_data.split("\n"):
            if row.strip() == "":
                continue

            array = row.split("#")

            # Prevent duplicate username (Bidder OR Seller)
            if len(array) >= 3 and array[2] == username:
                return render_template(
                    'BidderSignup.html',
                    data="❌ Username already exists"
                )

    # 💾 Save to blockchain
    data = f"Bidder#{name}#{username}#{password}#{address}#{number}#{email}\n"

    success = saveDataBlockChain(data, "adduser")

    if success:
        return render_template(
            "BidderSignup.html",
            data="✅ Bidder Registered Successfully"
        )
    else:
        return render_template(
            "BidderSignup.html",
            data="⚠ Blockchain Error. Try again."
        )


# ================= ADD SELLER =================

@app.route('/AddSellerAction', methods=['POST'])
def AddSellerAction():

    name = request.form.get('t1', '').strip()
    username = request.form.get('t2', '').strip()
    password = request.form.get('t3', '').strip()
    address = request.form.get('t4', '').strip()
    number = request.form.get('t5', '').strip()
    email = request.form.get('t6', '').strip()

    # 🔒 Basic Validation
    if not all([name, username, password, address, number, email]):
        return render_template(
            'SellerSignup.html',
            data="⚠ All fields are required"
        )

    # 🔎 Read existing users
    existing_data = readDetails('adduser')

    if existing_data:
        for row in existing_data.split("\n"):
            if row.strip() == "":
                continue

            array = row.split("#")

            # Prevent duplicate username (Bidder OR Seller)
            if len(array) >= 3 and array[2] == username:
                return render_template(
                    'SellerSignup.html',
                    data="❌ Username already exists"
                )

    # 💾 Save to blockchain
    data = f"Seller#{name}#{username}#{password}#{address}#{number}#{email}\n"

    success = saveDataBlockChain(data, "adduser")

    if success:
        return render_template(
            "SellerSignup.html",
            data="✅ Seller Registered Successfully"
        )
    else:
        return render_template(
            "SellerSignup.html",
            data="⚠ Blockchain Error. Try again."
        )
# ================= BIDDER LOGIN =================

@app.route('/BidderLogin', methods=['GET', 'POST'])
def BidderLogin():

    if request.method == 'GET':
        return render_template('BidderLogin.html')

    username = request.form.get('t1', '').strip()
    password = request.form.get('t2', '').strip()

    # 🔒 Basic validation
    if not username or not password:
        return render_template(
            'BidderLogin.html',
            data="⚠ Please enter Username and Password"
        )

    # Clear previous session
    session.pop('bidder', None)
    session.pop('recently_viewed', None)

    existing_data = readDetails('adduser')

    if existing_data:
        for row in existing_data.split("\n"):
            if row.strip() == "":
                continue

            array = row.split("#")

            if len(array) >= 4 and array[0] == 'Bidder' and array[2] == username and array[3] == password:
                session.pop('seller', None)
                session.pop('admin', None)
                session['bidder'] = username
                return render_template(
                    'BidderScreen.html',
                    data=f"✅ Welcome {username}"
                )

    return render_template(
        'BidderLogin.html',
        data="❌ Invalid Username or Password"
    )


# ================= SELLER LOGIN =================

@app.route('/SellerLoginAction', methods=['GET', 'POST'])
def SellerLoginAction():

    if request.method == 'GET':
        return render_template('SellerLogin.html')

    username = request.form.get('t1', '').strip()
    password = request.form.get('t2', '').strip()

    # 🔒 Basic validation
    if not username or not password:
        return render_template(
            'SellerLogin.html',
            data="⚠ Please enter Username and Password"
        )

    # Clear previous session
    session.pop('seller', None)

    existing_data = readDetails('adduser')

    if existing_data:
        for row in existing_data.split("\n"):
            if row.strip() == "":
                continue

            array = row.split("#")

            if len(array) >= 4 and array[0] == 'Seller' and array[2] == username and array[3] == password:
                session.pop('bidder', None)
                session.pop('admin', None)
                session['seller'] = username
                seller_dashboard = build_seller_dashboard(username)
                return _render_seller_dashboard_page(f"✅ Welcome {username}", seller_dashboard)
                return render_template(
                    'SellerScreen.html',
                    data=f"✅ Welcome {username}"
                )

    return render_template(
        'SellerLogin.html',
        data="❌ Invalid Username or Password"
    )


# ================= ADMIN LOGIN =================

@app.route('/AdminLogin', methods=['GET', 'POST'])
def AdminLogin():

    if request.method == 'GET':
        return render_template('AdminLogin.html')

    username = request.form.get('t1', '').strip()
    password = request.form.get('t2', '').strip()

    # 🔒 Validation
    if not username or not password:
        return render_template(
            'AdminLogin.html',
            data="⚠ Please enter Username and Password"
        )

    if username == 'admin' and password == 'admin':
        session.pop('bidder', None)
        session.pop('seller', None)
        session['admin'] = "admin"
        return render_template(
            'AdminScreen.html',
            data="✅ Welcome Admin"
        )

    return render_template(
        'AdminLogin.html',
        data="❌ Invalid Login Details"
    )
    # ================= ADD PRODUCT =================

@app.route('/AddProduct', methods=['GET', 'POST'])
def AddProduct():

    seller_name = session.get('seller')

    # 🔒 Seller must login
    if not seller_name:
        return render_template('SellerLogin.html', data="⚠ Please login first")

    # When user opens page
    if request.method == 'GET':
        return render_template('AddProduct.html')

    # Safe form access
    pid = request.form.get('t1', '').strip()
    pname = request.form.get('t2', '').strip()
    pinfo = request.form.get('t3', '').strip()
    price = request.form.get('t4', '').strip()
    file = request.files.get('t5')

    # 🔒 Validation
    if not all([pid, pname, pinfo, price]):
        return render_template('AddProduct.html', data="⚠ All fields are required")

    if not price.isdigit():
        return render_template('AddProduct.html', data="⚠ Price must be a number")

    if not file or file.filename == "":
        return render_template('AddProduct.html', data="❌ No file selected")

    # Create upload folder if not exists
    upload_folder = 'static/files/'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Unique filename (prevent overwrite)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # 🔎 Check duplicate Product ID
    existing_products = readDetails('product')

    if existing_products:
        for row in existing_products.split("\n"):
            if row.strip() == "":
                continue
            array = row.split("#")
            if array[0] == pid:
                return render_template(
                    'AddProduct.html',
                    data="❌ Product ID already exists"
                )

    # ⏳ Store auction creation time (for 1-hour auto close system)
    creation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to blockchain
    data = f"{pid}#{pname}#{pinfo}#{price}#{filename}#{seller_name}#{creation_time}\n"

    success = saveDataBlockChain(data, "product")

    if success:
        bidder_users = [row[2] for row in _get_user_records() if len(row) >= 7 and row[0] == "Bidder"]
        _broadcast_notification(bidder_users, {
            "id": _generate_transaction_id(),
            "type": "new_product",
            "message": f"New product added: {pname}.",
            "link": "/ViewProduct",
            "read": False,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "product_id": pid,
        })
        return render_template(
            'AddProduct.html',
            data="✅ Product Added Successfully (Auction time: 1 Hour)"
        )
    else:
        return render_template(
            'AddProduct.html',
            data="⚠ Blockchain Error"
        )


# ================= STATUS FUNCTION =================

def status(pid, pname, name):

    if not name:
        return False

    existing_history = readDetails('history')

    if existing_history:
        for row in existing_history.split("\n"):
            if row.strip() == "":
                continue

            array = row.split("#")

            # Safety length check
            if len(array) >= 4:
                if array[0] == pid and array[1] == pname and array[3] == name:
                    return True

    return False

# ================= VIEW PRODUCT =================

@app.route('/ViewProduct')
def ViewProduct():
    return _render_view_product_page()
    bidder_name = session.get('bidder')

    if not bidder_name:
        return render_template('BidderLogin.html', data="⚠ Please login first")

    output = '<table border="1" align="center" width="100%">'
    headers = ['Product ID','Product Name','Product Info','Base Price',
               'Highest Bid','Leading','Bidders','Photo','Time Left','Action']

    output += '<tr>'
    for header in headers:
        output += f'<th>{header}</th>'
    output += '</tr>'

    product_data = readDetails('product')
    history_data = readDetails('history')

    if not product_data:
        output += '</table><br/><br/>'
        return render_template('ViewProduct.html', data=output)

    # Convert history into structured list once (performance improvement)
    history_rows = []
    if history_data:
        history_rows = [
            row.split("#")
            for row in history_data.split("\n")
            if row.strip() != "" and len(row.split("#")) >= 5
        ]

    for row in product_data.split("\n"):

        if row.strip() == "":
            continue

        array = row.split("#")
        if len(array) < 7:
            continue

        pid = array[0]
        pname = array[1]
        pinfo = array[2]
        base_price = int(array[3])
        filename = array[4]
        creation_time = array[6]

        highest_bid = base_price
        leading_user = None
        bidders = set()

        # 🔥 Calculate highest bid & leader cleanly
        for harray in history_rows:

            if harray[0] == pid:
                amount = int(harray[4])
                user = harray[3]

                bidders.add(user)

                if amount > highest_bid:
                    highest_bid = amount
                    leading_user = user

        bidder_count = len(bidders)

        # ⏳ Auction timing
        auction_start = datetime.datetime.strptime(
            creation_time, "%Y-%m-%d %H:%M:%S"
        )
        auction_end = auction_start + datetime.timedelta(hours=1)
        auction_end_str = auction_end.strftime("%Y-%m-%d %H:%M:%S")

        output += '<tr>'
        output += f'<td>{pid}</td>'
        output += f'<td>{pname}</td>'
        output += f'<td>{pinfo}</td>'
        output += f'<td>₹{base_price}</td>'

        # 🔥 Highest Bid
        output += f'<td class="highest-bid" data-pid="{pid}">₹{highest_bid}</td>'

        # 🔥 Leading (ALWAYS raw username, JS decides badge)
        if leading_user:
            output += f'<td class="leader" data-pid="{pid}">{leading_user}</td>'
        else:
            output += f'<td class="leader" data-pid="{pid}">No Bids</td>'

        # 👥 Bidder Count
        output += f'<td class="bid-count" data-pid="{pid}">{bidder_count}</td>'

        output += f'<td><img src="static/files/{filename}" width="100"></td>'

        if datetime.datetime.now() < auction_end:
            output += f'<td><span class="timer" data-end="{auction_end_str}"></span></td>'
            output += f'<td><button type="button" class="bid-btn" data-pid="{pid}" data-pname="{pname}" data-filename="{filename}">Submit Bid</button></td>'
        else:
            output += '<td style="color:red;">⛔ Closed</td>'
            output += '<td><span class="btn btn-sm btn-secondary">Closed</span></td>'

        output += '</tr>'

    output += '</table><br/><br/>'

    return render_template('ViewProduct.html', data=output)

# ================= LIVE DATA API =================
from flask import jsonify

@app.route('/getLiveData')
def getLiveData():

    history_data = readDetails('history')
    product_data = readDetails('product')
    product_lookup = _get_product_lookup()
    now = datetime.datetime.now()

    live_data = {}
    recent_bids = []
    product_map = {}

    # 🔹 Build product id → product name map
    if product_data:
        for row in product_data.split("\n"):
            if row.strip() == "":
                continue
            arr = row.split("#")
            if len(arr) >= 2:
                product_map[arr[0]] = arr[1]

    # 🔹 Process history
    if history_data:
        rows = [r for r in history_data.split("\n") if r.strip() != ""]

        for row in rows:
            array = row.split("#")

            if len(array) >= 5:
                pid = array[0]
                user = array[3]
                amount = int(array[4])

                if pid not in live_data:
                    live_data[pid] = {
                        "highest": amount,
                        "leader": user,
                        "bidders": set([user])
                    }
                else:
                    live_data[pid]["bidders"].add(user)

                    if amount > live_data[pid]["highest"]:
                        live_data[pid]["highest"] = amount
                        live_data[pid]["leader"] = user

        # 🔥 Last 5 bids
        for row in rows[-5:]:
            arr = row.split("#")
            if len(arr) >= 5:
                recent_bids.append({
                    "pid": arr[0],
                    "user": arr[3],
                    "amount": arr[4]
                })

    # 🔹 Convert sets → JSON safe
    final_live = {}
    ranking = []

    for pid in live_data:
        product = product_lookup.get(pid)
        auction_end = _auction_end_from_product(product) if product else None
        auction_start = _parse_datetime(product.get("creation_time")) if product else None
        final_live[pid] = {
            "highest": live_data[pid]["highest"],
            "leader": live_data[pid]["leader"],
            "count": len(live_data[pid]["bidders"]),
            "endTs": int(auction_end.timestamp()) if auction_end else 0,
            "startTs": int(auction_start.timestamp()) if auction_start else 0,
            "status": _auction_status(auction_end, now),
            "progress": _auction_progress_percent(product, auction_end, now) if product else 0,
        }

        # Build ranking (one per product)
        if live_data[pid]["leader"]:
            ranking.append({
                "pid": pid,
                "product": product_map.get(pid, "Unknown"),
                "user": live_data[pid]["leader"],
                "amount": live_data[pid]["highest"]
            })

    # 🔥 Sort ranking by highest bid
    ranking.sort(key=lambda x: x["amount"], reverse=True)
    ranking = ranking[:5]

    return jsonify({
        "live": final_live,
        "recent": recent_bids,
        "ranking": ranking
    })


# ================= SUBMIT BID =================

@app.route('/Submitbid', methods=['GET', 'POST'])
def Submitbid():
    return _process_bid_submission()
    bidder_name = session.get('bidder')

    if not bidder_name:
        return render_template('BidderLogin.html', data="⚠ Please login first")

    if request.method == 'GET':
        return redirect(url_for('ViewProduct'))

    pid = request.form.get('pid')
    pname = request.form.get('pname')
    filename = request.form.get('filename')
    amount = request.form.get('t1', '').strip()

    if not amount.isdigit():
        return redirect(url_for('ViewProduct', bid_notice='invalid'))

    # 🔎 Check auction still active
    product_data = readDetails('product')

    for row in product_data.split("\n"):
        if row.strip() == "":
            continue

        array = row.split("#")
        if array[0] == pid and len(array) >= 7:
            creation_time = array[6]
            auction_start = datetime.datetime.strptime(creation_time, "%Y-%m-%d %H:%M:%S")
            auction_end = auction_start + datetime.timedelta(hours=1)

            if datetime.datetime.now() > auction_end:
                return redirect(url_for('ViewProduct', bid_notice='closed'))

    # 🚫 Prevent duplicate bid
    # if status(pid, pname, bidder_name):
        # return render_template('Submitbid.html', data="❌ You already submitted a bid")

    data = f"{pid}#{pname}#{filename}#{bidder_name}#{amount}\n"
    success = saveDataBlockChain(data, "history")

    if success:
        return redirect(url_for('ViewProduct', bid_notice='success'))
    else:
        return redirect(url_for('ViewProduct', bid_notice='error'))


# ================= GET PRODUCT ID (SELLER PRODUCTS) =================

def getproductid(name):

    product_ids = []
    product_data = readDetails('product')

    if product_data:
        for row in product_data.split("\n"):
            if row.strip() == "":
                continue

            array = row.split("#")

            if len(array) >= 6 and array[5] == name:
                product_ids.append(array[0])

    return product_ids


# ================= GET BIDDER NAMES =================

def getname():

    names = []
    history_data = readDetails('history')

    if history_data:
        for row in history_data.split("\n"):
            if row.strip() == "":
                continue

            array = row.split("#")

            if len(array) >= 4:
                names.append(array[3])

    return names

# ================= VIEW BID =================

@app.route('/ViewBid', methods=['GET'])
def ViewBid():

    seller_name = session.get('seller')

    if not seller_name:
        return render_template('SellerLogin.html', data="⚠ Please login first")

    product_ids = getproductid(seller_name)

    output = '<table border=1 align=center width=100%>'
    headers = ['Product ID','Product Name','Photo','Bidder Name','Amount Bidded']

    output += "<tr>"
    for header in headers:
        output += f"<th>{header}</th>"
    output += "</tr>"

    history_data = readDetails('history')

    bids = []

    if history_data:
        for row in history_data.split("\n"):
            if row.strip() == "":
                continue

            array = row.split("#")

            if len(array) >= 5 and array[0] in product_ids:
                bids.append(array)

    # 🔽 Sort bids highest first
    bids.sort(key=lambda x: int(x[4]), reverse=True)

    for array in bids:
        output += "<tr>"
        output += f"<td>{array[0]}</td>"
        output += f"<td>{array[1]}</td>"
        output += f'<td><img src="static/files/{array[2]}" width="100"></td>'
        output += f"<td>{array[3]}</td>"
        output += f"<td>{array[4]}</td>"
        output += "</tr>"

    output += "</table><br/><br/>"

    return render_template('ViewBid.html', data=output)


# ================= SELL =================

@app.route('/Sell', methods=['GET', 'POST'])
def Sell():

    seller_name = session.get('seller')

    if not seller_name:
        return render_template('SellerLogin.html', data="⚠ Please login first")

    return render_template(
        'SellerScreen.html',
        data="⚠ The Sell page has been removed from the seller workspace."
    )

    if request.method == 'GET':
        pid = getproductid(seller_name)
        return render_template('Sell.html', pid_all=pid)

    productid = request.form.get('pid')

    # 🔎 Check auction time finished
    product_data = readDetails('product')
    auction_valid = False

    if product_data:
        for row in product_data.split("\n"):
            if row.strip() == "":
                continue

            array = row.split("#")

            if len(array) >= 7 and array[0] == productid:
                creation_time = array[6]
                product = {
                    "pid": array[0],
                    "pname": array[1],
                    "pinfo": array[2],
                    "base_price": _safe_int(array[3]),
                    "filename": array[4],
                    "seller": array[5],
                    "creation_time": creation_time,
                }
                auction_end = _auction_end_from_product(product)

                if auction_end and datetime.datetime.now() >= auction_end:
                    auction_valid = True
                break

    if not auction_valid:
        return render_template('Sell.html', data="⛔ Auction Still Running (1 Hour Not Completed)")

    # 🔎 Prevent duplicate selling
    transaction_data = readDetails('transaction')
    if transaction_data:
        for row in transaction_data.split("\n"):
            if row.strip() == "":
                continue
            array = row.split("#")
            if len(array) >= 2 and array[0] == productid:
                return render_template('Sell.html', data="⚠ Product Already Sold")

    # 🔎 Select highest bidder
    history_data = readDetails('history')
    highest = 0
    winner = ""

    if history_data:
        for row in history_data.split("\n"):
            if row.strip() == "":
                continue
            array = row.split("#")

            if len(array) >= 5 and array[0] == productid:
                amount = int(array[4])
                if amount > highest:
                    highest = amount
                    winner = array[3]

    if winner:
        saveDataBlockChain(f"{productid}#{winner}\n", 'transaction')
        _append_notification(winner, {
            "id": _generate_transaction_id(),
            "type": "won",
            "message": f"You won the auction for {productid}.",
            "link": f"/Payment?product_id={productid}",
            "read": False,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "product_id": productid,
        })
        if seller_name:
            _append_notification(seller_name, {
                "id": _generate_transaction_id(),
                "type": "sold",
                "message": f"Auction sold for {productid} to {winner}.",
                "link": "/SellerScreen",
                "read": False,
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "product_id": productid,
            })
        return render_template('Sell.html', data=f"✅ Winner: {winner} (₹{highest})")
    else:
        return render_template('Sell.html', data="⚠ No bids placed for this product")


# ================= RESULT =================

@app.route('/Result', methods=['GET'])
def Result():

    bidder_name = session.get('bidder')

    if not bidder_name:
        return render_template('BidderLogin.html', data="⚠ Please login first")

    product_lookup = _get_product_lookup()
    payments = _payment_records_list()
    payment_lookup = {
        record.get("product_id"): record for record in payments if record.get("username") == bidder_name
    }

    # Get won products
    transaction_data = readDetails('transaction')
    won_products = []

    if transaction_data:
        for row in transaction_data.split("\n"):
            if row.strip() == "":
                continue
            array = row.split("#")
            if len(array) >= 2 and array[1] == bidder_name:
                won_products.append(array[0])

    # Get participated products
    history_data = readDetails('history')
    participated = []

    if history_data:
        for row in history_data.split("\n"):
            if row.strip() == "":
                continue
            array = row.split("#")
            if len(array) >= 4 and array[3] == bidder_name:
                if array[0] not in participated:
                    participated.append(array[0])

    # Generate table
    output = '<table class="table table-striped">'
    output += "<tr><th>Product ID</th><th>Product Name</th><th>Amount</th><th>Status</th><th>Payment</th></tr>"

    for pid in participated:
        product = product_lookup.get(pid, {})
        auction_end = _auction_end_from_product(product) if product else None
        auction_closed = bool(auction_end and datetime.datetime.now() >= auction_end)
        if pid in won_products:
            status = "🎉 WON"
        elif auction_closed:
            status = "❌ LOST"
        else:
            status = "⏳ LIVE"
        amount = "—"
        payment_cell = "—"
        if pid in won_products:
            snapshot = _get_bid_snapshot(pid)
            amount = f"₹{snapshot['highest_bid']}" if snapshot else "—"
            payment = payment_lookup.get(pid)
            if payment:
                payment_cell = f'Paid <a class="result-link" href="/Invoice/{payment["transaction_id"]}">View Invoice</a>'
            else:
                payment_cell = f'<a class="result-pay-btn" href="/Payment?product_id={pid}">Pay Now</a>'
        output += (
            f"<tr><td>{pid}</td>"
            f"<td>{product.get('pname', pid)}</td>"
            f"<td>{amount}</td>"
            f"<td>{status}</td>"
            f"<td>{payment_cell}</td></tr>"
        )

    output += "</table><br/><br/>"

    return render_template('Result.html', data=output)


@app.route('/Notifications', methods=['GET', 'POST'])
def Notifications():
    role, username = _get_user_context()
    if not username:
        if request.method == 'POST':
            return jsonify({"status": "error", "message": "Please login first"}), 401
        return render_template('BidderLogin.html', data="⚠ Please login first")

    if request.method == 'POST':
        ids = request.form.getlist('ids')
        if not ids and request.form.get('action') == 'read_all':
            ids = [item.get("id") for item in _get_notification_items(username)]
        _mark_notifications_read(username, ids)
        return jsonify({"status": "success"})

    notifications = _get_notification_items(username)
    unread_count = sum(1 for item in notifications if not item.get("read"))
    if request.args.get('format') == 'json':
        return jsonify({
            "status": "success",
            "unread_count": unread_count,
            "notifications": notifications[-10:][::-1],
        })

    return render_template(
        'Notifications.html',
        notifications=notifications[-20:][::-1],
        unread_count=unread_count,
        username=username,
        role=role or "User"
    )


@app.route('/Payment', methods=['GET', 'POST'])
def Payment():
    bidder_name = session.get('bidder')
    if not bidder_name:
        return render_template('BidderLogin.html', data="⚠ Please login first")

    product_id = request.values.get('product_id', '').strip()
    if not product_id:
        return redirect(url_for('Result'))

    product_lookup = _get_product_lookup()
    product = product_lookup.get(product_id)
    if not product:
        return redirect(url_for('Result'))

    existing_payment = _payment_for_product(product_id, bidder_name)
    if existing_payment:
        return redirect(url_for('Invoice', transaction_id=existing_payment["transaction_id"]))

    snapshot = _get_bid_snapshot(product_id)
    if not snapshot or snapshot["leader"] != bidder_name:
        return render_template('Result.html', data="⚠ Only the winning bidder can make payment.")

    if request.method == 'GET':
        return render_template(
            'Payment.html',
            product=product,
            winning_amount=snapshot["highest_bid"],
            payment=existing_payment
        )

    card_number = request.form.get('card_number', '').strip().replace(' ', '')
    card_holder = request.form.get('card_holder', '').strip()
    expiry = request.form.get('expiry', '').strip()
    cvv = request.form.get('cvv', '').strip()

    if not (card_number.isdigit() and 13 <= len(card_number) <= 19):
        return render_template('Payment.html', product=product, winning_amount=snapshot["highest_bid"], error="Invalid card number")
    if not card_holder or len(card_holder) < 3:
        return render_template('Payment.html', product=product, winning_amount=snapshot["highest_bid"], error="Invalid card holder name")
    if not cvv.isdigit() or len(cvv) not in (3, 4):
        return render_template('Payment.html', product=product, winning_amount=snapshot["highest_bid"], error="Invalid CVV")

    expiry_match = re.match(r"^(0[1-9]|1[0-2])\/(\d{2}|\d{4})$", expiry)
    if not expiry_match:
        return render_template('Payment.html', product=product, winning_amount=snapshot["highest_bid"], error="Invalid expiry date")

    month = int(expiry_match.group(1))
    year = int(expiry_match.group(2))
    if year < 100:
        year += 2000
    today = datetime.date.today()
    if (year, month) < (today.year, today.month):
        return render_template('Payment.html', product=product, winning_amount=snapshot["highest_bid"], error="Card expired")

    transaction_id = _generate_transaction_id()
    payment_record = {
        "transaction_id": transaction_id,
        "product_id": product_id,
        "product_name": product["pname"],
        "username": bidder_name,
        "amount": snapshot["highest_bid"],
        "card_holder": card_holder,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Paid",
    }

    payments = _load_payments()
    payments[transaction_id] = payment_record
    _save_payments(payments)
    _append_notification(bidder_name, {
        "id": transaction_id,
        "type": "payment",
        "message": f"Payment successful for {product['pname']}.",
        "link": f"/Invoice/{transaction_id}",
        "read": False,
        "created_at": payment_record["date"],
        "product_id": product_id,
    })

    return redirect(url_for('Invoice', transaction_id=transaction_id))


@app.route('/Invoice/<transaction_id>')
def Invoice(transaction_id):
    if not (session.get('bidder') or session.get('seller') or session.get('admin')):
        return render_template('BidderLogin.html', data="⚠ Please login first")

    payments = _load_payments()
    payment = payments.get(transaction_id) if isinstance(payments, dict) else None
    if not payment:
        return render_template('Result.html', data="⚠ Invoice not found")

    return render_template('Invoice.html', payment=payment)


@app.route('/BidChart/<product_id>')
def BidChart(product_id):
    if not (session.get('bidder') or session.get('seller') or session.get('admin')):
        return render_template('BidderLogin.html', data="⚠ Please login first")

    product_lookup = _get_product_lookup()
    product = product_lookup.get(product_id)
    if not product:
        return render_template('Result.html', data="⚠ Product not found")

    history_rows = _get_history_rows_with_meta()
    chart_rows = [row for row in history_rows if row["pid"] == product_id]
    chart_rows.sort(key=lambda item: item.get("time") or "")

    return render_template(
        'BidChart.html',
        product=product,
        chart_rows=chart_rows
    )


@app.route('/SuspiciousBids')
def SuspiciousBids():
    if not session.get('admin'):
        return render_template('AdminLogin.html', data="⚠ Admin Login Required")

    analysis = _suspicious_bid_analysis()
    return render_template(
        'SuspiciousBids.html',
        suspicious_records=analysis["records"],
    )


@app.route('/EditProfile', methods=['GET', 'POST'])
def EditProfile():
    profile = _build_profile()
    if not profile:
        return render_template('BidderLogin.html', data="⚠ Please login first")

    if profile["role"] not in {"Bidder", "Seller"}:
        return render_template('Profile.html', profile=profile, error="Profile editing is available for bidders and sellers only.")

    latest_row = _latest_user_record(profile["username"])
    if request.method == 'GET':
        return render_template('EditProfile.html', profile=profile, user_row=_build_user_payload(latest_row))

    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()

    if not all([name, email, phone, address]):
        return render_template('EditProfile.html', profile=profile, user_row=_build_user_payload(latest_row), error="All fields are required")
    if "@" not in email or "." not in email:
        return render_template('EditProfile.html', profile=profile, user_row=_build_user_payload(latest_row), error="Invalid email address")
    if not phone.isdigit() or len(phone) < 8:
        return render_template('EditProfile.html', profile=profile, user_row=_build_user_payload(latest_row), error="Invalid phone number")

    if not latest_row:
        return render_template('EditProfile.html', profile=profile, user_row=None, error="User record not found")

    updated_row = f"{profile['role']}#{name}#{profile['username']}#{latest_row[3]}#{address}#{phone}#{email}\n"
    saveDataBlockChain(updated_row, "adduser")
    _append_notification(profile["username"], {
        "id": _generate_transaction_id(),
        "type": "profile",
        "message": "Profile updated successfully.",
        "link": "/Profile",
        "read": False,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    return redirect(url_for('Profile', role=profile["role"]))

# ================= VIEW SELLER =================

@app.route('/ViewSeller', methods=['GET'])
def ViewSeller():

    # 🔒 Admin only access
    if not session.get('admin'):
        return render_template('AdminLogin.html', data="⚠ Admin Login Required")

    output = '<table border="1" align="center" width="100%">'
    headers = ['Name','Username','Password','Address','Number','Email']

    output += '<tr>'
    for header in headers:
        output += f'<th>{header}</th>'
    output += '</tr>'

    user_data = readDetails('adduser')

    if user_data:
        for row in user_data.split("\n"):
            if row.strip() == "":
                continue

            array = row.split("#")

            if len(array) >= 7 and array[0] == 'Seller':
                output += '<tr>'
                output += f'<td>{array[1]}</td>'
                output += f'<td>{array[2]}</td>'
                output += f'<td>********</td>'  # 🔒 Hide password
                output += f'<td>{array[4]}</td>'
                output += f'<td>{array[5]}</td>'
                output += f'<td>{array[6]}</td>'
                output += '</tr>'

    output += '</table><br/><br/>'

    return render_template('ViewSeller.html', data=output)


# ================= VIEW BIDDER =================

@app.route('/ViewBidder', methods=['GET'])
def ViewBidder():

    # 🔒 Admin only access
    if not session.get('admin'):
        return render_template('AdminLogin.html', data="⚠ Admin Login Required")

    output = '<table border="1" align="center" width="100%">'
    headers = ['Name','Username','Password','Address','Number','Email']

    output += '<tr>'
    for header in headers:
        output += f'<th>{header}</th>'
    output += '</tr>'

    user_data = readDetails('adduser')

    if user_data:
        for row in user_data.split("\n"):
            if row.strip() == "":
                continue

            array = row.split("#")

            if len(array) >= 7 and array[0] == 'Bidder':
                output += '<tr>'
                output += f'<td>{array[1]}</td>'
                output += f'<td>{array[2]}</td>'
                output += f'<td>********</td>'  # 🔒 Hide password
                output += f'<td>{array[4]}</td>'
                output += f'<td>{array[5]}</td>'
                output += f'<td>{array[6]}</td>'
                output += '</tr>'

    output += '</table><br/><br/>'

    return render_template('ViewBidder.html', data=output)


# ================= VIEW TRANSACTION =================

@app.route('/ViewTransaction', methods=['GET'])
def ViewTransaction():

    # 🔒 Admin only access
    if not session.get('admin'):
        return render_template('AdminLogin.html', data="⚠ Admin Login Required")

    output = '<table border="1" align="center" width="100%">'
    headers = ['Product ID', 'Bidder who won']

    output += '<tr>'
    for header in headers:
        output += f'<th>{header}</th>'
    output += '</tr>'

    transaction_data = readDetails('transaction')

    if transaction_data:
        for row in transaction_data.split("\n"):
            if row.strip() == "":
                continue

            array = row.split("#")

            if len(array) >= 2:
                output += '<tr>'
                output += f'<td>{array[0]}</td>'
                output += f'<td>{array[1]}</td>'
                output += '</tr>'

    output += '</table><br/><br/>'

    return render_template('ViewTransaction.html', data=output)
# ================= BASIC PAGE ROUTES =================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')


# ================= SELLER ROUTES =================

@app.route('/SellerLogin')
def SellerLoginPage():
    return render_template('SellerLogin.html')


@app.route('/SellerScreen')
def SellerScreenPage():
    return _render_seller_dashboard_page()


@app.route('/SellerEarnings')
def SellerEarnings():
    return _render_seller_dashboard_page()


@app.route('/SellerAnalytics')
def SellerAnalytics():
    seller_name = session.get('seller')
    if not seller_name:
        return render_template('SellerLogin.html', data="âš  Please login first")

    analytics = build_seller_analytics(seller_name)
    return _render_seller_dashboard_page(
        f"âœ… Analytics loaded for {seller_name}",
        build_seller_dashboard(seller_name)
    )


@app.route('/BidHistory')
def BidHistory():
    if not session.get('bidder'):
        return render_template('BidderLogin.html', data="⚠ Please login first")

    profile = _build_profile()
    history_rows = _get_history_rows_with_meta()

    bidder_history = [row for row in history_rows if row['bidder'] == profile['username']]
    bidder_history.sort(key=lambda item: item.get('time') or "", reverse=True)

    return render_template(
        'BidHistory.html',
        profile=profile,
        history_rows=bidder_history
    )


@app.route('/Leaderboard')
def Leaderboard():
    if not (session.get('bidder') or session.get('seller') or session.get('admin')):
        return render_template('BidderLogin.html', data="⚠ Please login first")

    return render_template(
        'Leaderboard.html',
        leaderboard=_build_leaderboard()
    )


@app.route('/Profile')
def Profile():
    role_hint = request.args.get('role', '').strip().title() or None
    if role_hint not in {"Bidder", "Seller", "Admin"}:
        role_hint = None

    profile = _build_profile(role_hint=role_hint)
    if not profile:
        return render_template('BidderLogin.html', data="⚠ Please login first")

    return render_template('Profile.html', profile=profile)


@app.route('/TrackViewed', methods=['POST'])
def TrackViewed():
    bidder_name = session.get('bidder')
    if not bidder_name:
        return jsonify({"status": "error", "message": "Please login as a bidder first"}), 401

    pid = request.form.get('pid', '').strip()
    if not pid or pid not in _get_product_lookup():
        return jsonify({"status": "error", "message": "Invalid product"}), 400

    _track_recently_viewed_product(pid)
    return jsonify({"status": "success", "pid": pid})


@app.route('/RecentlyViewed')
def RecentlyViewed():
    bidder_name = session.get('bidder')
    if not bidder_name:
        return render_template('BidderLogin.html', data="⚠ Please login first")

    return render_template(
        'RecentlyViewed.html',
        bidder_name=bidder_name,
        recently_viewed_products=_build_recently_viewed_products()
    )


@app.route('/BidderAnalytics')
def BidderAnalytics():
    bidder_name = session.get('bidder')
    if not bidder_name:
        return render_template('BidderLogin.html', data="⚠ Please login first")

    return render_template(
        'BidderScreen.html',
        data=f"✅ Analytics ready for {bidder_name}",
        bidder_analytics=_build_bidder_analytics(bidder_name),
        recently_viewed_products=_build_recently_viewed_products(),
        trending_products=_build_trending_auctions()
    )


@app.route('/Trending')
def Trending():
    if not session.get('bidder'):
        return render_template('BidderLogin.html', data="⚠ Please login first")

    return render_template(
        'Trending.html',
        trending_products=_build_trending_auctions()
    )


@app.route('/AddWatchlist', methods=['POST'])
def AddWatchlistRoute():
    bidder_name = session.get('bidder')
    if not bidder_name:
        return jsonify({"status": "error", "message": "Please login as a bidder first"}), 401

    pid = request.form.get('pid', '').strip()
    if not pid or pid not in _get_product_lookup():
        return jsonify({"status": "error", "message": "Invalid product"}), 400

    _add_watchlist_item(bidder_name, pid)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.accept_mimetypes.best == "application/json":
        return jsonify({"status": "success", "message": "Added to watchlist", "pid": pid})
    return redirect(url_for('ViewWatchlistRoute'))


@app.route('/ViewWatchlist')
def ViewWatchlistRoute():
    bidder_name = session.get('bidder')
    if not bidder_name:
        return render_template('BidderLogin.html', data="âš  Please login first")

    watched_ids = _get_watchlist_for_user(bidder_name)
    product_lookup = _get_product_lookup()
    watchlist_rows = []
    now = datetime.datetime.now()

    for pid in watched_ids:
        product = product_lookup.get(pid)
        if not product:
            continue

        snapshot = _get_bid_snapshot(pid)
        auction_end = snapshot['auction_end'] if snapshot else _auction_end_from_product(product)
        watchlist_rows.append({
            "pid": pid,
            "pname": product["pname"],
            "pinfo": product["pinfo"],
            "base_price": product["base_price"],
            "highest_bid": snapshot["highest_bid"] if snapshot else product["base_price"],
            "leader": snapshot["leader"] if snapshot else "",
            "status": _auction_status(auction_end, now),
            "auction_end": auction_end.strftime("%d-%m-%Y %I:%M %p") if auction_end else "Unavailable",
            "remaining": _format_remaining_time(auction_end, now),
            "filename": product["filename"],
        })

    return render_template(
        'ViewWatchlist.html',
        watchlist_rows=watchlist_rows,
        bidder_name=bidder_name
    )


@app.route('/AdminAnalytics')
def AdminAnalytics():
    if not session.get('admin'):
        return render_template('AdminLogin.html', data="⚠ Admin Login Required")

    return render_template(
        'AdminScreen.html',
        data="✅ Admin analytics ready",
        admin_analytics=_build_admin_analytics()
    )


@app.route('/SellerSignup')
def SellerSignupPage():
    return render_template('SellerSignup.html')


@app.route('/SellerLogout')
def SellerLogout():
    session.pop('seller', None)
    return render_template('SellerLogin.html', data="✅ Logged out successfully")


# ================= BIDDER ROUTES =================

@app.route('/BidderLoginPage')
def BidderLoginPage():
    return render_template('BidderLogin.html')


@app.route('/BidderScreenPage')
def BidderScreenPage():
    if not session.get('bidder'):
        return render_template('BidderLogin.html', data="⚠ Please login first")
    bidder_name = session.get('bidder')
    return render_template(
        'BidderScreen.html',
        data=f"Welcome {bidder_name}.",
        bidder_analytics=_build_bidder_analytics(bidder_name),
        recently_viewed_products=_build_recently_viewed_products(),
        trending_products=_build_trending_auctions()
    )


@app.route('/BidderSignupPage')
def BidderSignupPage():
    return render_template('BidderSignup.html')


@app.route('/BidderSignup')
def BidderSignupRoute():
    return render_template('BidderSignup.html')


@app.route('/BidderLogout')
def BidderLogout():
    session.pop('bidder', None)
    return render_template('BidderLogin.html', data="✅ Logged out successfully")


# ================= ADMIN ROUTES =================

@app.route('/AdminLoginPage')
def AdminLoginPage():
    return render_template('AdminLogin.html')


@app.route('/AdminScreen')
def AdminScreen():
    if not session.get('admin'):
        return render_template('AdminLogin.html', data="⚠ Admin Login Required")
    return render_template(
        'AdminScreen.html',
        admin_analytics=_build_admin_analytics()
    )


@app.route('/AdminLogout')
def AdminLogout():
    session.pop('admin', None)
    return render_template('AdminLogin.html', data="✅ Logged out successfully")


# ================= SAFE PAGE ACCESS ROUTES =================

@app.route('/ViewTransactionPage')
def ViewTransactionPage():
    if not session.get('admin'):
        return render_template('AdminLogin.html', data="⚠ Admin Login Required")
    return redirect(url_for('ViewTransaction'))


@app.route('/ViewBidderPage')
def ViewBidderPage():
    if not session.get('admin'):
        return render_template('AdminLogin.html', data="⚠ Admin Login Required")
    return redirect(url_for('ViewBidder'))


@app.route('/ViewSellerPage')
def ViewSellerPage():
    if not session.get('admin'):
        return render_template('AdminLogin.html', data="⚠ Admin Login Required")
    return redirect(url_for('ViewSeller'))


@app.route('/ResultPage')
def ResultPage():
    if not session.get('bidder'):
        return render_template('BidderLogin.html', data="⚠ Please login first")
    return render_template('Result.html')


@app.route('/SellPage')
def SellPage():
    if not session.get('seller'):
        return render_template('SellerLogin.html', data="⚠ Please login first")
    return render_template(
        'SellerScreen.html',
        data="⚠ The Sell page has been removed from the seller workspace."
    )


@app.route('/ViewBidPage')
def ViewBidPage():
    if not session.get('seller'):
        return render_template('SellerLogin.html', data="⚠ Please login first")
    return render_template('ViewBid.html')


@app.route('/SubmitbidPage')
def SubmitBidPage():
    if not session.get('bidder'):
        return render_template('BidderLogin.html', data="⚠ Please login first")
    return redirect(url_for('ViewProduct'))


@app.route('/ViewProductPage')
def ViewProductPage():
    if not session.get('bidder'):
        return render_template('BidderLogin.html', data="⚠ Please login first")
    return render_template('ViewProduct.html')


@app.route('/AddProductPage')
def AddProductPage():
    if not session.get('seller'):
        return render_template('SellerLogin.html', data="⚠ Please login first")
    return render_template('AddProduct.html')


# ================= RUN APP =================

if __name__ == '__main__':
    app.run(debug=False)
