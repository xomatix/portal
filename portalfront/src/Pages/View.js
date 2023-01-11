import React from 'react';

class View extends React.Component {
    state = {
        data : []
    }

    async componentDidMount() {
        try {
            const resp = await fetch(process.env.REACT_APP_API_URL + '/category');
            const data = await resp.json();
            this.setState({data: data});
            console.log(this.state);
        }   catch (err) {
            console.log(err);
        }
        
    }

    render() {
        const {data} = this.state;
        return (
            <div className='View'>
                <ul>
                    {
                        data.map((item)=>{
                            return <li>{item.name}</li>
                        })
                    }
                </ul>
            </div>
        );
    }
}

export default View;