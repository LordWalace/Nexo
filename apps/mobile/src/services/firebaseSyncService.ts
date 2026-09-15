import { doc, setDoc, getDoc, collection, getDocs } from 'firebase/firestore';
import { db, auth } from '../config/firebase';
import { Activity, Category, Material, HistorySession } from '../stores/useDataStore';

export const syncToFirestore = async (
  collectionName: 'activities' | 'categories' | 'materials' | 'history',
  data: any[]
) => {
  const user = auth.currentUser;
  if (!user) return; // Only sync if logged in

  try {
    const collectionDocRef = doc(db, `users/${user.uid}/appData`, collectionName);
    await setDoc(collectionDocRef, { data });
  } catch (error) {
    console.error(`Erro ao sincronizar ${collectionName} com Firestore:`, error);
  }
};

export const syncFromFirestore = async (
  collectionName: 'activities' | 'categories' | 'materials' | 'history'
) => {
  const user = auth.currentUser;
  if (!user) return null;

  try {
    const collectionDocRef = doc(db, `users/${user.uid}/appData`, collectionName);
    const docSnap = await getDoc(collectionDocRef);
    if (docSnap.exists()) {
      return docSnap.data().data; // Retorna o array
    }
  } catch (error) {
    console.error(`Erro ao buscar ${collectionName} do Firestore:`, error);
  }
  return null;
};
