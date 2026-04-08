# Secure Online E-Auction System using Blockchain Technology

## 📋 Overview

A comprehensive blockchain-based online auction platform built with Flask and Solidity. This system provides a secure, decentralized environment for conducting auctions with transparent transaction records, real-time bidding, and advanced fraud detection mechanisms.

---

## 🎯 Key Features

### 1. **User Management**

#### User Roles
- **Bidders** - Users who participate in auctions by placing bids on products
- **Sellers** - Users who list products for auction and manage their inventory
- **Administrators** - System administrators with oversight and monitoring capabilities

#### Authentication & Registration
- Secure user registration for bidders and sellers
- Role-based authentication system
- Unique username validation to prevent duplicate accounts
- Admin dashboard with hardcoded credentials (username: `admin`, password: `admin`)
- Session management with role-based access control
- User profile management and editing capabilities

### 2. **Product Listing & Management**

#### Product Features
- **Product Creation** - Sellers can list new products with:
  - Unique Product ID
  - Product Name and Description
  - Base/Starting Bid Price
  - Product Images (file upload support)
  - Automatic seller attribution
  - Timestamp tracking (creation time)

#### Product Categorization
- Automatic category inference based on product name and description
- Supported Categories:
  - Electronics (phones, laptops, cameras, tablets)
  - Fashion (clothing, accessories, watches, jewelry)
  - Vehicles (cars, bikes, motorcycles)
  - Real Estate (houses, flats, plots, villas)
  - Art & Antiques (vintage items, paintings, sculptures)
  - Sports (equipment, recreational gear)
  - Agriculture (fruits, vegetables, grains)

#### Product Viewing
- Comprehensive product display with pagination (10 products per page)
- Real-time product information including:
  - Product ID, Name, and Category
  - Detailed product information
  - Base price and highest current bid
  - Leading bidder information
  - Number of active bidders
  - Product images
  - Auction end time
  - Live auction status indicators

### 3. **Auction Management**

#### Auction Lifecycle
- **Duration** - 1-hour default auction period per product
- **Real-time Updates** - Live bid tracking and updates
- **Auction States** - Active, Ending Soon (≤5 minutes remaining), and Closed
- **Time Extensions** - Automatic 2-minute extension when bids received within final 2 minutes
- **Progress Tracking** - Visual progress bars showing auction completion percentage
- **Countdown Timers** - Real-time countdown display for remaining auction time

#### Auction Status Display
- Live bidding status indicators
- Auction progress percentage visualization
- Formatted countdown timers (hours, minutes, seconds)
- Closed auction indicators
- "Ending Soon" alerts for auctions in final 5 minutes

### 4. **Bidding System**

#### Core Bidding Features
- **Minimum Bid Increment** - ₹10 rule to prevent trivial increments
- **Bid Placement** - Real-time bid submission with validation
- **Bid History** - Complete bidding history tracking with:
  - Bid amount and timestamp
  - Previous bids from same user
  - Product information linked to bid
  - Bidder identification
  - Chronological bid records

#### Bid Validation
- Prevents bids lower than base price
- Enforces minimum bid increment over highest bid
- Validates bids on closed auctions
- Checks product information integrity
- Automatic auction extension on late bids

#### Bid Notifications
- Outbid alerts sent to previous leading bidders
- Real-time notification system
- Bid status messages (success, failure, invalid, closed)

#### Bidding Analytics (for Bidders)
- Total bids placed
- Auctions participated in
- Auctions won
- Win rate calculation
- Recently viewed products tracking

### 5. **Transaction Management**

#### Transaction Processing
- **Winner Determination** - Automatic identification of auction winners
- **Transaction Recording** - Blockchain-recorded transactions linking:
  - Product ID
  - Winning bidder name
  - Final winning bid amount
  - Transaction timestamp
  
#### Transaction Details
- Complete transaction history viewing (Admin only)
- Product ID to winner mapping
- Bid amount records
- Transaction status tracking

### 6. **Watchlist & Recently Viewed**

#### Watchlist Features
- Add/remove products from personal watchlist
- Persistent watchlist storage (JSON-based)
- Quick access to watched auctions
- Watchlist status indicators on product listings
- Maximum watched items optimization

#### Recently Viewed Products
- Automatic tracking of up to 5 recently viewed products
- Quick access to previously viewed auctions
- Enhanced browsing experience
- Session-based storage with persistence

### 7. **Advanced Analytics & Dashboards**

#### Bidder Dashboard
- **Personalized Analytics:**
  - Total bids placed
  - Number of auctions participated in
  - Number of auctions won
  - Win rate percentage
  - Recently viewed products count
  
- **Trending Auctions Display:**
  - Top 5 trending products by bidding activity
  - Bid count rankings
  - Highest bid tracking
  - Bid increase calculations
  - Current leading bidders
  - Time remaining display

#### Seller Dashboard
- **Performance Analytics:**
  - Total products listed
  - Total products sold
  - Total earnings calculation
  - Highest selling product identification
  - Average bid per product
  
- **Sales Management:**
  - Complete sold products list with:
    - Product name
    - Winning bidder
    - Winning bid amount
  - Sorted by winning bid price (descending)
  - Product listing status tracking

#### Admin Dashboard
- **System-wide Analytics:**
  - Total registered users count
  - Total products listed
  - Total bids placed
  - Total completed transactions
  - System health monitoring
  
- **Comprehensive Views:**
  - All registered bidders
  - All registered sellers
  - All products and their details
  - Complete transaction history
  - Bid history analysis

### 8. **Fraud Detection System**

#### Suspicious Bidding Detection
Automated detection algorithms identifying suspicious activity patterns:

1. **Rapid Bidding Pattern** - Multiple bids in succession (≤60 seconds apart)
2. **Aggressive Stack Bidding** - 3+ bids on same product within 5 minutes
3. **Unusual Bid Jumps** - Bid amounts increasing by 75% or more from previous bid
4. **Late Night Activity** - Automated timestamping for pattern analysis

#### Suspicious Bids Dashboard
- Display of flagged bids and bidders
- Detailed reason for suspicion marking
- Product association tracking
- Time and amount logging
- User activity flags
- Admin review interface

#### Protective Measures
- Visual indicators for suspicious activity
- Highlighted rows for suspicious bids/bidders
- Detailed audit trail
- Historical pattern analysis
- Recommendation system for review

### 9. **Notifications System**

#### Notification Types
- **Outbid Notifications** - When another bidder surpasses your bid
- **Auction Status** - Updates on auction endings and results
- **System Messages** - Important platform announcements
- **Transaction Alerts** - Bid placement confirmations

#### Notification Management
- Read/unread status tracking
- Notification creation timestamp
- Product linking for context
- Clickable navigation to related auctions
- Persistent notification history
- Bulk notification operations

### 10. **Blockchain Integration**

#### Smart Contract Features
- **Solidity Contract (Auction.sol)** with functions for:
  - User data management (`addUsers()`, `getUsers()`)
  - Product information storage (`addproduct()`, `getproduct()`)
  - Bid history tracking (`addhistory()`, `gethistory()`)
  - Transaction records (`addtransaction()`, `gettransaction()`)

#### Blockchain Connectivity
- Web3.py integration for Ethereum connectivity
- HTTP RPC provider communication
- Transaction receipt verification
- Block timestamp recording
- Gas transaction management
- Default account handling for contract calls

#### Data Persistence
- All user data stored on blockchain
- All products recorded on blockchain
- All bid history immutably logged
- All transactions recorded with blockchain timestamps
- Decentralized data storage ensuring transparency

### 11. **Payment & Revenue Management**

#### Payment Tracking
- Payment record storage for completed transactions
- Payment status tracking
- Transaction ID generation
- Revenue recording per transaction
- Payment history per user

#### Revenue Management
- Seller earnings calculation
- Total transaction values
- Payment settlement tracking
- Revenue analytics per seller
- Transaction-level payment details

### 12. **Search & Filter Capabilities**

#### Product Search
- Real-time product table searching
- Search by product name
- Search by category
- Multi-criteria filtering

#### Filtering Options
- Filter by auction status (Active, Ending Soon, Closed)
- Filter by price range (base price, highest bid)
- Filter by bidding activity
- Filter by auction progress
- Sort by multiple criteria

### 13. **Bid Chart & Visualization**

#### Bid Chart Features
- Visual representation of bidding history
- Chart display for each product
- Bid progression over time
- Bidder participation metrics
- Historical bid tracking
- Time-based analysis

### 14. **Leaderboard System**

#### Top Bidders Leaderboard
- Top 10 bidders by bid count
- Ranking with bid frequency
- Active bidder identification
- Competitive statistics
- Performance metrics

### 15. **Profile & Account Management**

#### User Profiles
- Complete user information display
- Role identification
- Contact information (email, phone)
- Address storage
- Activity statistics:
  - For Bidders: total bids, auctions participated, won
  - For Sellers: total bids, auctions won, products listed

#### Profile Editing
- Update personal information
- Modify contact details
- Change address information
- Account security management

### 16. **Responsive Image Management**

#### Image Upload & Storage
- Product image file upload support
- Storage in `static/files/` directory
- Image preview in product listings
- Multiple image format support
- Efficient image retrieval and display

### 17. **Session Management**

#### Session Features
- Role-based session storage (bidder, seller, admin)
- Session isolation between roles
- Automatic session cleanup on role switch
- Secure session key generation
- Session state persistence

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.2.5
- **Language**: Python
- **Blockchain**: Solidity (Smart Contracts)
- **Blockchain Connection**: Web3 5.12.2
- **Database**: Blockchain (Ethereum network on localhost)

### Frontend
- **Templates**: HTML/Jinja2
- **Styling**: Bootstrap, CSS
- **JavaScript**: jQuery, Custom JS
- **UI Components**: Bootstrap components, Charts.js, Lightbox
- **Date/Time**: Moment.js, DateRangePicker

### Build & Development
- **Smart Contract Compilation**: Truffle Framework
- **Contract Deployment**: Truffle Migrations
- **Package Management**: pip (Python)

### Dependencies
```
numpy==1.19.5
pandas==0.25.1
web3==5.12.2
flask==2.2.5
itsdangerous==2.1.0
werkzeug==0.16.0
markupsafe==2.1.1
```

---

## 📁 Project Structure

```
Secure Online E-Auction System using Blockchain Technology/
├── app.py                          # Main Flask application
├── Auction.json                    # Compiled contract ABI
├── truffle-config.js              # Truffle configuration
├── run.bat                         # Run script (Windows)
│
├── contracts/                      # Smart Contracts
│   ├── Auction.sol               # Main auction contract
│   └── Migrations.sol            # Migration contract
│
├── migrations/                     # Truffle migrations
│   ├── 1_initial_migration.js
│   └── 2_deploy_contracts.js
│
├── build/                          # Compiled contracts
│   └── contracts/
│       ├── Auction.json
│       └── Migrations.json
│
├── static/                         # Static files
│   ├── assets/
│   │   ├── css/                  # Stylesheets
│   │   ├── js/                   # JavaScript files
│   │   ├── fonts/                # Web fonts
│   │   ├── images/               # Static images
│   │   └── webfonts/             # Font files
│   └── files/                    # Uploaded product images
│       ├── bid_history_meta.json
│       ├── notifications.json
│       ├── payments.json
│       ├── watchlist.json
│       └── auction_extensions.json
│
├── templates/                      # HTML templates
│   ├── index.html                # Home page
│   ├── AdminLogin.html
│   ├── AdminScreen.html
│   ├── BidderLogin.html
│   ├── BidderScreen.html
│   ├── BidderSignup.html
│   ├── SellerLogin.html
│   ├── SellerScreen.html
│   ├── SellerSignup.html
│   ├── AddProduct.html
│   ├── ViewProduct.html
│   ├── ViewBid.html
│   ├── Submitbid.html
│   ├── Sell.html
│   ├── Result.html
│   ├── ViewBidder.html
│   ├── ViewSeller.html
│   ├── ViewTransaction.html
│   ├── Profile.html
│   ├── EditProfile.html
│   ├── Notifications.html
│   ├── BidChart.html
│   ├── Leaderboard.html
│   ├── SuspiciousBids.html
│   ├── Trending.html
│   ├── Watchlist.html
│   ├── Payment.html
│   ├── Invoice.html
│   ├── BidHistory.html
│   ├── RecentlyViewed.html
│   └── Navigation templates (admin_nav.html, bidder_nav.html, seller_nav.html)
│
└── proposed/                       # Alternative/proposed versions
    ├── app.py
    ├── Auction.json
    └── [Similar structure as main folder]
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Node.js & npm (for Truffle)
- Ganache or local Ethereum node running on port 8545
- Git

### Installation

1. **Clone or Download the Repository**
   ```bash
   cd "Secure Online E-Auction System using Blockchain Technology"
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r proposed/requirements.txt
   ```

3. **Install Truffle (for smart contracts)**
   ```bash
   npm install -g truffle
   ```

4. **Start Local Blockchain**
   ```bash
   ganache-cli --host 127.0.0.1 --port 8545
   ```

5. **Deploy Smart Contracts**
   ```bash
   truffle migrate
   ```

6. **Run the Application**
   ```bash
   python app.py
   ```
   or on Windows:
   ```bash
   run.bat
   ```

7. **Access the Application**
   - Open browser and navigate to `http://localhost:5000`

---

## 📝 Usage Guide

### For Bidders
1. **Register** - Sign up with your details on the BidderSignup page
2. **Login** - Log in with your credentials
3. **Browse Products** - View available auctions on the dashboard
4. **Place Bids** - Submit bids on products of interest
5. **Track Progress** - Monitor bid status and winning positions
6. **View Results** - Check won auctions in the Results section

### For Sellers
1. **Register** - Sign up as a seller
2. **Login** - Access your seller dashboard
3. **List Products** - Add new products with details and images
4. **View Bids** - Monitor incoming bids on your products
5. **Sell Products** - Finalize sales with winning bidders
6. **Analytics** - Track earnings and selling performance

### For Admins
1. **Login** - Use admin credentials (admin/admin)
2. **Monitor System** - View all users, products, and transactions
3. **View Analytics** - System-wide statistics and metrics
4. **Review Fraud** - Monitor suspicious bidding patterns
5. **Manage Data** - Oversee all blockchain records

---

## 🔒 Security Features

- **Blockchain-based** - Immutable transaction records
- **Role-based Access Control** - Separate dashboards for bidders, sellers, admins
- **Input Validation** - HTML/SQL injection prevention
- **Unique Usernames** - Prevents duplicate account registration
- **Timestamp Recording** - Block-level timestamps for auctions
- **Suspicious Activity Detection** - Fraud prevention mechanisms
- **Session Security** - Role-specific session management

---

## 📊 Key Metrics & Data Points

### User Data
- User Role (Bidder/Seller/Admin)
- Name, Username, Password (hashed on blockchain)
- Address, Phone, Email
- Registration timestamp

### Product Data
- Product ID, Name, Description
- Base Price, Highest Bid
- Seller Information
- Creation timestamp
- Category (auto-inferred)

### Bid Data
- Bid ID, Product ID, Amount
- Bidder Name, Timestamp
- Bid Status (accepted/rejected)
- Historical tracking

### Transaction Data
- Transaction ID, Product ID
- Winner Name, Winning Amount
- Transaction Timestamp
- Payment Status

---

## 🔄 Update & Maintenance

### Database Maintenance
- JSON file cleanup for large watchlist/notification files
- Periodic blockchain snapshot review
- Contract upgrade procedures

### Monitoring
- Check Ganache logs for transaction errors
- Monitor Flask application logs
- Review blockchain gas usage

---

## 📞 Support & Troubleshooting

### Common Issues

**Issue**: Blockchain connection refused
- **Solution**: Ensure Ganache is running on port 8545

**Issue**: Contract not found
- **Solution**: Run `truffle migrate` to deploy contracts

**Issue**: File upload failed
- **Solution**: Check `static/files/` directory permissions

**Issue**: Bid not recorded
- **Solution**: Verify Ganache has sufficient gas and active accounts

---

## 📄 License

This project is provided as-is for educational and commercial purposes.

---

## 👥 Contributors

- **Development Team**: Secure Auction System Contributors
- **Project**: Secure Online E-Auction System using Blockchain Technology
- **Version**: 2.0

---

## 🎓 Educational Value

This project demonstrates:
- ✅ Smart contract development and deployment
- ✅ Blockchain integration with web applications
- ✅ Full-stack web development (Flask + JavaScript)
- ✅ Real-time auction system design
- ✅ Fraud detection algorithms
- ✅ Advanced data analytics implementation
- ✅ Responsive web design
- ✅ Session management and authentication

---

## 🔮 Future Enhancements

Potential features for future versions:
- [ ] Payment gateway integration (Stripe, Razorpay)
- [ ] Email verification for user registration
- [ ] Advanced reporting and analytics
- [ ] Mobile application
- [ ] Automated auction closing and winner notification
- [ ] Seller rating and review system
- [ ] Secure messaging between bidders and sellers
- [ ] Integration with other blockchain networks
- [ ] Machine learning for fraud detection enhancement
- [ ] Real-time WebSocket updates

---

## 📞 Contact & Support

For questions, issues, or suggestions, please refer to the project documentation or contact the development team.

---

**Last Updated**: April 2026
**Status**: Active Development
