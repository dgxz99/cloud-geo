// server/config/neo4jConfig.js
const neo4j = require("neo4j-driver");

// 创建 Neo4j 驱动程序实例
const driver = neo4j.driver(
    "bolt://localhost:7687",
    neo4j.auth.basic("neo4j", "12345678") // 使用你的Neo4j用户名和密码
);

driver.onCompleted = () => {
    console.log("Neo4j connection established.");
};

driver.onError = (error) => {
    console.error("Neo4j connection error:", error);
};

module.exports = driver;
