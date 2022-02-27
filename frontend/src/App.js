import './App.css';
import Keyboard from './keyboard';
import {useState, useEffect, useCallback} from 'react';
import midijson from './snowflake.json';

function App() {

  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  const onResize = useCallback(() => {
    setSize({
      width: window.innerWidth,
      height: window.innerHeight
    })
  }, []);

  useEffect(() => {
    window.addEventListener('resize', onResize);
    return (() => {
      window.removeEventListener('resize', onResize);
    })
  }, []);

  return (
    <div className="App">
      <Keyboard width={size.width} height={size.height} midijson={midijson}/>
    </div>
  );
}

export default App;
