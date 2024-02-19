db.createUser({
    user: "askstyler",
    pwd: "Styler_12345",
    roles: [{ role: "readWrite", db: "mydatabase" }]
  });