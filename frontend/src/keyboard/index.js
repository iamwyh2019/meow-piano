import './keyboard.css'
import {useState, useEffect} from 'react'

const Keyboard = ({width, height}) => {
    // white : black = 39:27 = 13:9
    // nWhite = 51, nBlack = 36, total 987 units
    // wWhite = width / 987 * 13, wBlack = width / 987 * 9
    // White w:h = 39:198 = 13:66, Black w:h = 27:126 = 9:42
    // 52 gaps, 52px
    const unit = (width-52) / 987;
    const wWhite = unit*13, wBlack = unit*9;
    const hWhite = unit*66, hBlack = unit*42;

    const whites = [...Array(51).keys()]

    const whiteEles = whites.map((ele, index) => {
        const whiteStyle = {
            width: wWhite,
            height: hWhite,
            left: index*wWhite + index + 1,
        };
        return <div className="white" key={index} style={whiteStyle}></div>
    });

    const blackStyle = {
        width: wBlack,
        height: hBlack,
    };

    return (
        <div className="keyboard">
            {whiteEles}
        </div>
    )
}

export default Keyboard