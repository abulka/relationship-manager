using System;
using System.Collections.Generic;
using System.Text;

namespace RelationshipManager.Turbo
{

    class CallCache
    {
        public static bool cacheEnabled = true;

        protected bool cachedDataIsRealData = false;

        public void Invalidate()
        {
            cachedDataIsRealData = false;
        }
    }

    class CallCacheObjStrObj : CallCache
    {
        private object paramObj = null;
        private string paramStr;
        private object resultObj = null;

        public object Result
        {
            get { return resultObj; }
        }

        public void SetData(object paramObj, string paramStr, object resultObj)
        {
            this.paramObj = paramObj;
            this.paramStr = paramStr;
            this.resultObj = resultObj;
            cachedDataIsRealData = true;
        }

        public bool CallMatches(object fromObj, string relId)
        {
            return (cacheEnabled &&
                cachedDataIsRealData &&
                this.paramObj == fromObj &&
                this.paramStr == relId);
        }

    }



    class CallCacheStrInt : CallCache
    {
        private string paramStr;
        private int resultInt;

        public int Result
        {
            get { return resultInt; }
        }

        public void SetData(string paramStr, int resultInt)
        {
            this.paramStr = paramStr;
            this.resultInt = resultInt;
            cachedDataIsRealData = true;
        }

        public bool CallMatches(string paramStr)
        {
            return (cacheEnabled &&
                cachedDataIsRealData &&
                this.paramStr == paramStr);
        }

    }


    class CallCacheInt : CallCache
    {
        private int resultInt;

        public int Result
        {
            get { return resultInt; }
        }

        public void SetData(int resultInt)
        {
            this.resultInt = resultInt;
            cachedDataIsRealData = true;
        }

        public bool CallMatches()
        {
            return (cacheEnabled &&
                cachedDataIsRealData);
        }

    }

}




/*
 * 
 * EXPERIMENTATION WITH GENERICS
 * 
 * 
    public class Cache<T> where T: new()
    {
        private T cache;
        private bool valid = false;

        public T Value
        {
            get
            {
                return cache;
            }

            set
            {
                cache = value;
                valid = true;
            }
        }

        public bool IsValid
        {
            get
            {
                return valid;
            }
        }

        public void Invalidate()
        {
            valid = false;
        }

    }


    public class TestCache
    {
        public TestCache()
        {
            LastCall = new Cache<IntInt>();
            LastCall.Value = new IntInt();
            LastCall.Invalidate();
        }

        private int RawFactorial(int i)
        {
            if (i > 1)
            {
                return i * RawFactorial(i - 1);
            }
            else
            {
                return 1;
            }
        }

        private Cache<IntInt> LastCall;

        private int Product(int i, int x)
        {
            if (!LastCall.IsValid || (LastCall.Value.MatchArguments(i, x)))
            {
                LastCall.Value.Set(i, x, RawProduct(i,x));
                LastCall.MarkAsValid();
            }

            return LastCall.Value.Result;
        }


    }

    public class IntIntInt
    {
        public int Argument1, Argument2, Result;

        public void Set (int arg1, int arg2, int result)
        {
            Argument1 = arg1;
            Argument2 = arg2;
            Result = result;
        }

        public bool MatchArguments(int arg1, int arg2)
        {
            return arg1 == Argument1 && arg2 == Argument2;
        }
    }




        private object paramObj = null;
        private string paramStr;
        private object resultObj = null;

        public override bool Equals(object obj)
        {
            if (obj is ObjStrObj)
            {
                ObjStrObj other = obj as ObjStrObj;

                return (p1 == other.p1) && (p2 == other.p2) &&;
            }

            return false;
        }

    }


    public class ObjStrObj
    {
        private object paramObj = null;
        private string paramStr;
        private object resultObj = null;

        public override bool Equals(object obj)
        {
            if (obj is ObjStrObj)
            {
                ObjStrObj other = obj as ObjStrObj;

                return (p1 == other.p1) && (p2 == other.p2) &&;
            }

            return false;
        }

    }


    public class OptimizedCacheObjStrObj : Cache<GC>
    {

    }

    public class CacheCallFindObjectPointedToByMe2
    {
        private object fromObj = null;
        public string relId;
        public object result = null;

        private bool cachedDataIsRealData = false;
        public bool cacheEnabled = true;

        public void SetData(object fromObj, string relId, object result)
        {
            this.fromObj = fromObj;
            this.relId = relId;
            this.result = result;
            cachedDataIsRealData = true;
        }

        public bool CallMatches(object fromObj, string relId)
        {
            return (cacheEnabled &&
                cachedDataIsRealData &&
                this.fromObj == fromObj &&
                this.relId == relId);
        }

        public void Invalidate()
        {
            cachedDataIsRealData = false;
        }
    }

}
*/

