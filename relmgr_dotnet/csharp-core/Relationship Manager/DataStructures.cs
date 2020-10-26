using System;
using System.Collections;
using System.Text;

using RelationshipManager.Interfaces;  // for the backpointer to rm in Links class

namespace RelationshipManager.Turbo
{

    public interface IToObjs
    {
        int Count { get; }
        void Add(object obj);
        void Remove(object obj);
        bool Contains(object obj);
        object GetFirstHashKey();
        ArrayList ToArray();
    }

    public enum LinksDirection
    {
        Forward,
        Backward
    }

    class HashColl
    {
        public Hashtable Value = new Hashtable();

        public void Clear()
        {
            Value.Clear();
        }
        public void Add(object obj)
        {
            Value[obj] = true;
        }
        public void Remove(object obj)
        {
            Value.Remove(obj);
        }
        public object GetFirstHashKey()
        {
            IEnumerator e = Value.Keys.GetEnumerator();
            if (e.MoveNext())
                return e.Current;
            else
                return null;
        }
        public ArrayList ToArray()
        {
            return new ArrayList(Value.Keys);
        }
        public bool Contains(object obj)
        {
            return Value.Contains(obj);
        }
        public int Count
        {
            get { return Value.Count; }
        }
    }



    class ToObjs : HashColl, IToObjs
    {
    }

    class ToObjsSingle : IToObjs
    {
        private object ToObj;
        private bool IsEmpty = true;

        public int Count 
        { 
            get 
            {
                if (IsEmpty)
                    return 0;
                else
                    return 1;
            }
        }
        public void Add(object obj) 
        { 
            ToObj = obj;
            IsEmpty = false;
        }
        public void Remove(object obj)
        {
            ToObj = null;
            IsEmpty = true;
        }

        /// <summary>
        /// See if obj matches the toobj
        /// </summary>
        /// <param name="obj"></param>
        /// <returns></returns>
        /// Be careful when using relationship manager to
        /// maintain relationships between value types
        /// i.e. ints and strings and chars etc. since these
        /// will be auto converted to unique boxed object 
        /// instances and you may not be able to ever 
        /// match that generated value!!
        /// 
        /// The solution is to always store object instances
        /// which is always the case with class instances. 
        /// Strings work out ok since they always get mapped
        /// to the same immutable address anyway, so using
        /// value types in this case is safe.  
        /// Value type of char and int are a problem, so please
        /// convert these to boxed version before storing.
        /// 
        /// (Note the one to many implementation which 
        /// uses a hashtable doesn't suffer this
        /// implementation nuance because of the way hashtable
        /// keys seems work. e.g. storing a value type char
        /// as a key in a hashtable will always match with 
        /// a totally different value type char, as long as 
        /// it is the same 'value'.).
        public bool Contains(object obj)
        {
            bool match = (obj == ToObj);
            return (!IsEmpty && match);
        }

        public object GetFirstHashKey()
        {
            if (!IsEmpty)
                return ToObj;
            else
                //throw new Exception("No value in ToObjs object");
                return null;
        }

        public ArrayList ToArray()
        {
            ArrayList result = new ArrayList();
            if (!IsEmpty)
                result.Add(ToObj);
            return result;
        }
    }

    class RelIds : HashColl
    {
        IToObjs result;

        public IToObjs FindToObjs(string relId)
        {
            result = (IToObjs)Value[relId];
            return result;
        }
        public void SetEntry(string relId, IToObjs toObj)
        {
            Value[relId] = toObj;
        }
    }

    class Links : HashColl
    {
        RelIds result;
        private RelationshipMgrTurbo rm;
        private LinksDirection linksDirection;

        public Links(RelationshipMgrTurbo rm, LinksDirection linksDirection)
        {
            this.rm = rm;
            this.linksDirection = linksDirection;
        }

        public RelIds FindRelIds(object fromObj)
        {
            result = (RelIds)Value[fromObj];
            return result;
        }

        public RelIds GetRelIdsHashTable(object fromObj, bool repairIfNotThere)
        {
            RelIds relIds;
            if (this.Contains(fromObj))
                relIds = this.FindRelIds(fromObj);
            else
            {
                relIds = new RelIds();
                if (repairIfNotThere)
                    this.SetEntry(fromObj, relIds);
            }
            return relIds;

        }
        public IToObjs GetToObjs(object fromObj, string relId)
        {
            RelIds relIds;
            IToObjs toObjs;

            relIds = this.GetRelIdsHashTable(fromObj, true);

            if (relIds.Contains(relId))
                toObjs = relIds.FindToObjs(relId);
            else
            {
                Cardinality cardinality = rm.LookUpCardinality(relId);

                if (rm.optimiseOneToOne)
                {
                    if (cardinality == Cardinality.OneToOne ||
                        cardinality == Cardinality.OneToMany && this.linksDirection == LinksDirection.Backward ||
                        cardinality == Cardinality.ManyToOne && this.linksDirection == LinksDirection.Forward )
                        toObjs = new ToObjsSingle();
                    else
                        toObjs = new ToObjs();
                }
                else
                    toObjs = new ToObjs();
                
                relIds.SetEntry(relId, toObjs);
            }

            return toObjs;
        }

        public void SetEntry(object fromObj, RelIds relIds)
        {
            Value[fromObj] = relIds;
        }
    }



    
}
