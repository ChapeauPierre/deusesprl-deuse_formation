import React, {useState} from 'react';

export default function HelloWorld({
    message,
}) {
    const [count, setCount] = useState(0);

    const incCounter = () => {
        setCount(count + 1);
    }

    return (
        <>
            <p>Dataset Message: {message}</p>
            <p>Counter: {count}</p>
            <button onClick={incCounter}>Add</button>
        </>
    )
}