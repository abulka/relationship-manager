using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

using RelationshipManager56;
using RelationshipManager.Interfaces;

namespace BooFormTest01
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        #region ANDYCODE

        private void print()
        {
            print("");
        }

        private void print(string s)
        {
            textBox1.AppendText(s + "\n");
        }

        private void Test01()
        {
            print();

            RM1 rm = new RM1();
            print(rm.ToString());
            print();

            rm.ER("xtoy", Cardinality.OneToOne, Directionality.DirectionalWithBackPointer);
            rm.R("andy", "boo", "xtoy");
        }

        private void Test02_Person()
        {
            print("--------- Person ->* Order --------------");
            print();
            Person p1 = new Person("Andy");
            Person p2 = new Person("Jim");
            print(p1.ToString());
            print(p2.ToString());

            Order o1 = new Order("widget A");
            Order o2 = new Order("widget B");
            Order o3 = new Order("widget C");
            print(o1.ToString());
            print(o2.ToString());
            print(o3.ToString());
            print();

            p1.AddOrder(o1);
            p1.AddOrder(o2);
            print("Orders for " + p1.ToString() + " are:");
            foreach (Order o in p1.GetOrders())
            {
                print(o.ToString());
            }

            print();
            print("Who ordered widget " + o1.ToString() + " ?  Answer is");
            print(o1.GetPerson().ToString());
        }

        #endregion

        private void Form1_Load(object sender, EventArgs e)
        {
            this.Test01();
            this.Test02_Person();
        }



    }

}