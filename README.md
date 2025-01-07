# RNA-seq Metadata Application

## 1. What Works? 🚀

### ✅ **Backend**  
- **Python-based backend** using FastAPI.  
- **RDF data creation and insertion** into GraphDB.  
- **Queries to fetch RDF data** from GraphDB.  
- Successfully **stored and retrieved sample metadata** in RDF format.  

### ✅ **Frontend**  
- **React app** built with Vite.  
- **Dev server running** and serving the app at [http://localhost:5173](http://localhost:5173).  
- Environment set up for **API calls** and **dynamic data rendering**.  

### ✅ **Database (GraphDB)**  
- Installed and running on [http://localhost:7200](http://localhost:7200).  
- Repository (**mesyto_repo**) created and operational.  
- **SPARQL queries executed successfully** to check data in both default and named graphs.  
- **Schema and sample data inserted and verified** in RDF format.  

### ✅ **RDF Utilities**  
- **Functions to create RDF data models** using `rdflib`.  
- **Stored RDF data** using `SPARQLWrapper` and `requests`.  
- **Fetch and query operations** work seamlessly with GraphDB.  

---

## 2. Technologies Used ⚙️

### **Backend:**  
- **Python (v3.10+)**  
- **FastAPI** - Web framework for backend APIs.  
- **rdflib** - RDF data processing.  
- **SPARQLWrapper** - Querying RDF databases.  
- **requests** - HTTP communication with GraphDB.  

### **Frontend:**  
- **React** - Frontend framework.  
- **Vite** - Build tool for fast development.  
- **Axios** - HTTP requests to backend APIs.  

### **Database:**  
- **GraphDB** - Triple store database for RDF storage and queries.  

### **Environment Management:**  
- **Virtualenv** - Python dependency isolation.  
- **Node.js + npm** - JavaScript package management.  

### **Security Tests:**  
- Environment structured for future **penetration tests** and **upload restrictions**.  
- Endpoints secured with **validation utilities** and **input sanitization**.  

---

## 3. Getting Started 🛠️

### **Prerequisites**
- **Python 3.10+** installed.  
- **Node.js (v16+)** and **npm (v8+)** installed.  
- **GraphDB Desktop Edition** or Server Edition installed and running.  

---

### **1. Clone Repository:**
```bash
git clone git@github.com:yourusername/metomics.git
cd mesyto
```

### **2. Backend Setup:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Linux/MacOS

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **3. Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

### 4. GraphDB Setup 🗄️

1. **Launch GraphDB**  
   Open GraphDB by navigating to:  
   [http://localhost:7200](http://localhost:7200)

2. **Create a Repository**  
   - Go to the **Repositories** tab.  
   - Click **Create new repository**.  
   - Select the **Repository Type** (e.g., **GraphDB-SE**).  
   - Set the **Repository ID** to `mesyto_repo`.  
   - Click **Create** to finalize.

3. **Verify the Repository**  
   Ensure the repository is accessible at:  
   [http://localhost:7200/repositories/mesyto_repo](http://localhost:7200/repositories/mesyto_repo)

