CREATE TABLE user (
    user_id VARCHAR(300) PRIMARY KEY,
    user_name TEXT
);

CREATE TABLE product (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    discounted_price DECIMAL(10,2),
    actual_price DECIMAL(10,2),
    discount_percentage VARCHAR(10), 
    rating DECIMAL(3,2),
    about_product TEXT,
    img_link TEXT,
    product_link TEXT
);

CREATE TABLE review (
    review_id VARCHAR(300) PRIMARY KEY,
    review_title TEXT,
    review_content TEXT,
    user_id VARCHAR(300),
    product_id VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);


CREATE INDEX idx_review_user_id ON review(user_id);

CREATE INDEX idx_review_product_id ON review(product_id);
