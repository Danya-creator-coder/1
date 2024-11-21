from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import create_engine, String, Float
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column

app = Flask(__name__)

# Налаштування бази даних
DB_URL = "sqlite:///pizza.db"
engine = create_engine(DB_URL, echo=True)

class Base(DeclarativeBase):
    pass

class Pizza(Base):
    __tablename__ = "pizzas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(200))
    price: Mapped[int] = mapped_column()

def init_db():
    Base.metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']


        with Session(engine) as session:
            new_pizza = Pizza(name=name, description=description, price=price)
            session.add(new_pizza)
            session.commit()
            return redirect(url_for('success'))

    return render_template('admin.html')

@app.route('/success/')
def success():
    return render_template('success.html')

@app.route('/pizzas/')
def pizzas():
    with Session(engine) as session:
        pizza_list = session.query(Pizza).all()
        print(pizza_list)
        return render_template('pizzas.html', pizzas=pizza_list)

if __name__ == '__main__':
    init_db()
    app.run(port=5002, debug=True)