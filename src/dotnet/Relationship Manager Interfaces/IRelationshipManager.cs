using System;
using System.Collections.Generic;
using System.Collections;
using System.Text;

namespace RelationshipManager.Interfaces
{
    public enum Cardinality
    {
        OneToOne,
        OneToMany,
        ManyToOne,
        ManyToMany
    }

    public enum Directionality
    {
        UniDirectional,
        DirectionalWithBackPointer,
        DoubleDirectional
    }

    public interface IRelationshipManager
    {
        void AddRelationship(object fromObj, object toObj, string relId);
        void AddRelationship(object fromObj, object toObj);
        //void EnforceRelationship(string relId, string cardinality);
		//void EnforceRelationship(string  relId, string cardinality, string directionality);
        void EnforceRelationship(string relId, Cardinality cardinality);
        void EnforceRelationship(string relId, Cardinality cardinality, Directionality directionality);
        IList FindObjectsPointedToByMe(object fromObj, string relId);
		object FindObjectPointedToByMe(object fromObj, string relId);
	 	IList FindObjectsPointingToMe(object toObj, string relId);
		object FindObjectPointingToMe(object toObj, string relId);
		void RemoveRelationship(object fromObj, object toObj, string relId);
		void RemoveAllRelationshipsInvolving(object obj, string relId);
        int Count();
        int CountRelationships(string relId);
        void Clear();
        bool DoesRelIdExistBetween(object fromObj, object toObj, string relId);
        IList FindRelIdsBetween(object fromObj, object toObj);
    }

    public interface IRM
    {
        object B(object toObj, string relId);
        System.Collections.IList BS(object toObj, string relId);
        void ER(string relId, Cardinality cardinality);
        void ER(string relId, Cardinality cardinality, Directionality directionality);
        void NR(object fromObj, object toObj, string relId);
        void NRS(object obj, string relId);
        object P(object fromObj, string relId);
        System.Collections.IList PS(object fromObj, string relId);
        void R(object fromObj, object toObj, string relId);
        bool QR(object fromObj, object toObj, string relId);
        int Count();
        int CountRelationships(string relId);
        void Clear();
    }
}
