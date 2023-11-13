import React, { useEffect, useState } from 'react';
import { Image } from 'react-native';
import styled from 'styled-components/native';
import firebase from 'firebase';

if (!firebase.apps.length) {
  firebase.initializeApp({
    apiKey: 'AIzaSyCMqsgrxQAIDgTWsBGO82OdnrexgP9MHnU',
    authDomain: 'presencepulse-oficial.firebaseapp.com',
    projectId: 'presencepulse-oficial',
    storageBucket: 'presencepulse-oficial.appspot.com',
    messagingSenderId: '306876529614',
    appId: '1:306876529614:web:82231a266e98701de1099f',
    databaseURL: 'https://presencepulse-oficial-default-rtdb.firebaseio.com',
  });
}

const imagem_fundo = () =>{ 
    return 'https://picsum.photos/200/300?grayscale'
}

const db = firebase.database();

const Container = styled.View`
  flex: 1;
  align-items: center;
  background-color: ${(props) => props.bgColor || '#fff'};
  justify-content: center;
`;

const DataText = styled.Text`
  font-size: 20px;
  color: #fff;
  background-color: #222;
  padding: 10px;
  margin-top: 20px;
`;

export default function App() {
  const [data, setData] = useState(null);
  const [previousDistance, setPreviousDistance] = useState(null);
  const [backgroundColor, setBackgroundColor] = useState('#333');



  const generateDarkColor = () => {
    let color = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
    while (color.length < 7) color += '0';
    return color;
  };

  useEffect(() => {
    const dbRef = db.ref('Teste/Dados');
    dbRef.on('value', (snapshot) => {
      const firebaseData = snapshot.val();
      if (firebaseData) {
        const parsedData = JSON.parse(firebaseData);
        if (parsedData && parsedData.presenca && parsedData.distancia) {
          setData(parsedData);
          if (parsedData.distancia !== previousDistance) {
            setBackgroundColor(generateDarkColor());
            setPreviousDistance(parsedData.distancia);
          }
        } else {
          console.log('Dados incompletos:', parsedData);
        }
      } else {
        console.log('Dados não encontrados.');
      }
    });

    return () => {
      dbRef.off('value');
    };
  }, [previousDistance]);

  return (
    <Container bgColor={backgroundColor}>
      {data ? (
        <>
          {data.imagem && (
            <Image
              source={{ uri: `data:image/jpeg;base64,${data.imagem}` }}
              style={{ width: 200, height: 200 }}
            />
            
          )}
          <DataText>
            Presença: {data.presenca} - Distância: {data.distancia}cm
          </DataText>
        </>
      ) : (
        <DataText>Carregando dados...{console.log(data)}</DataText>
      )}
    </Container>
  );
}
