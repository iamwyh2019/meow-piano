import './keyboard.css'
import {useState, useEffect} from 'react'
import keyboard_layout from './position'

const Keyboard = ({width, height, midijson}) => {
    // white : black = 39:27 = 13:9
    // nWhite = 51, nBlack = 36, white 663 units
    // wWhite = width / 987 * 13, wBlack = width / 987 * 9
    // White w:h = 39:198 = 13:66, Black w:h = 27:126 = 9:42
    // 52 gaps, 52px
    const unit = (width-54) / 663;
    const wWhite = unit*13, wBlack = unit*9;
    const hWhite = unit*66, hBlack = unit*42;

    const keyboard_eles = keyboard_layout.map((ele, index) => {
        if (ele.white) {
            const whiteStyle = {
                width: wWhite,
                height: hWhite,
                left: ele.offset*(wWhite+1) + 1,
            };
            return (
                <div className="white" style={whiteStyle} key={index}>
                    <div className="kbnote">{ele.name}</div>
                </div>
            )
        }
        else {
            const blackStyle = {
                width: wBlack,
                height: hBlack,
                left: ele.offset*(wWhite+1) + 2 - wBlack/2,
                bottom: (hWhite-hBlack+2) + 'px',
            };
            return <div className="black" style={blackStyle} key={index}></div>
        }
    });

    return (
        <div className="keyboard">
            {keyboard_eles}
        </div>
    )
}

export default Keyboard