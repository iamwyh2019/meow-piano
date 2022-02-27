import './keyboard.css'
import keyboard_layout from './position'
import Cat from './cats';
import React, { useEffect, useState } from 'react';

const Keyboard = ({width, height, midijson}) => {
    // white : black = 39:27 = 13:9
    // nWhite = 51, nBlack = 36, white 663 units
    // wWhite = width / 987 * 13, wBlack = width / 987 * 9
    // White w:h = 39:198 = 13:66, Black w:h = 27:126 = 9:42
    // 52 gaps, 52px
    const unit = (width-54) / 663;
    const wWhite = unit*13, wBlack = unit*9;
    const hWhite = unit*66, hBlack = unit*42;
    const catOffset = height/10 + hWhite;

    const wLeft = (offset) => offset*(wWhite+1)+1;
    const bLeft = (offset) => offset*(wWhite+1)+2-wBlack/2;

    const keyboard_eles = keyboard_layout.map((ele, index) => {
        if (ele.white) {
            const whiteStyle = {
                width: wWhite,
                height: hWhite,
                left: wLeft(ele.offset),
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
                left: bLeft(ele.offset),
                bottom: hWhite - hBlack + 2,
            };
            return (
                <div className="black" style={blackStyle} key={index}></div>
            )
        }
    });

    const cat_eles = keyboard_layout.map((ele, index) => {
        if (ele.white) {
            return (
                <Cat className="Cat" cat_width={wWhite} 
                    left={wLeft(ele.offset)} bottom={catOffset}
                    key={index+keyboard_layout.length}/>
            )
        }
        else {
            return (
                <Cat className="Cat" cat_width={wWhite} 
                    left={bLeft(ele.offset)} bottom={catOffset+hWhite}
                    key={index+keyboard_layout.length}/>
            )
        }
    });

    const duration = Math.max(...midijson.map(d => d.offset_time));


    return (
        <div className="keyboard">
            {keyboard_eles}
            {cat_eles}
        </div>
    )
}

export default Keyboard