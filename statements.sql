CREATE TABLE products (
    id SERIAL PRIMARY KEY,                       
    main_category VARCHAR(255),                 
    title VARCHAR(255),                         
    average_rating FLOAT,                       
    rating_number INT,                          
    features VARCHAR,                             
    description VARCHAR,                          
    price FLOAT,                                
    store VARCHAR(255),                         
    parent_asin VARCHAR(255) UNIQUE NOT NULL            
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,                       
    rating FLOAT,                                
    title VARCHAR(255),                          
    text TEXT,                                   
    asin VARCHAR(255),                           
    parent_asin VARCHAR(255),                    
    user_id VARCHAR(255),                        
    created_at BIGINT,                              
    verified_purchase BOOLEAN,                   
    helpful_vote INT,                            
    FOREIGN KEY (parent_asin) REFERENCES products(parent_asin) ON DELETE CASCADE
);
