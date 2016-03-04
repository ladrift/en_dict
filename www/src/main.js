var ExampleList = React.createClass({
    render: function() {
        var examples = this.props.data.map(function(example) {
            return (
                <li><p>
                {example.sentence} {example.translation}
                </p>
                </li>
            )
        });
        return (
            <div className="wordExampleList">
            <h4>例句</h4>
            {examples}
            </div>
        );
    }
});

var MeaningList = React.createClass({
    render: function() {
        var meanings = this.props.data.map(function(meaning) {
            return (
                <li><p>
                {meaning.part_of_speech} {meaning.explanation}
                </p>
                </li>
            )
        });
        return (
            <div className="wordExplanationList">
            {meanings}
            </div>
        );
    }
});

var SearchResult = React.createClass({
    render: function() {
        var item = this.props.item;
        if (item == null) {
            return (
                <div className="panel panel-default">
                <div className="panel-heading">
                <h3 className="panel-title">Explanation</h3>
                </div>
                <div className="panel-body">
                </div>
                </div>
            );
        } else {
            console.log(item);
            return (
                <div className="panel panel-default">
                <div className="panel-heading">
                <h3 className="panel-title">Explanation</h3>
                </div>
                <div className="panel-body">
                <h2>{item.word}</h2>
                <MeaningList data={item.meanings} />
                <ExampleList data={item.examples} />
                </div>
                </div>
            );
        }
    }
});

var SearchButton = React.createClass({
    render: function() {
        return (
            <button className="btn btn-info" type="button" onClick={this.props.onSearch}>
            <span className="glyphicon glyphicon-search" aria-hidden="true"></span>
            </button>
        );
    }
});

var LoadingButton = React.createClass({
    render: function() {
        return (
            <button className="btn btn-info" type="button">
            <img src='static/img/loading.gif' style={{width: '18px'}}/>
            </button>
        )
    }
});

var DropdownList = React.createClass({
    render: function() {
        var words = this.props.recommendWords.map(word => (
                <li><a onClick={this.props.onWordSelect}>
                {word}
                </a>
                </li>
            )
        );
        if (words.length > 0) {
            return (
                <div className={this.props.isOpen ? "dropdown open" : "dropdown"}>
                <ul className="dropdown-menu">
                    {words.slice(0, 10)}
                </ul>
                </div>
            );
        }
        else {
            return (
                <div className={this.props.isOpen ? "dropdown open" : "dropdown"}>
                <ul className="dropdown-menu">
                    <li><a>No word to recommend...</a></li>
                </ul>
                </div>

            );
        }
    }
});

var SearchInput = React.createClass({
    getInitialState: function() {
        return {
            word: '',
            recommendWords: [],
            isRecommendOpen: false,
        };
    },
    handleWordChange: function(e) {
        this.setState({word: e.target.value});

        // Grab the recommend words from /api/recommend

        if (e.target.value.length > 0) {
            this.setState({isRecommendOpen: true});
            $.ajax({
                url: '/api/recommend',
                dataType: 'json',
                contentType: 'application/json',
                type: 'POST',
                data: JSON.stringify({word: e.target.value}),
                success: function(data) {
                    console.log(data);
                    if (data.words == undefined) {
                        this.setState({recommendWords: []})
                    }
                    else {
                        this.setState({recommendWords: data.words})
                    }
                }.bind(this),
                error: function(xhr, status, err) {
                    console.error('/api/recommend', status. err.toString());
                }.bind(this)
            });
        }
        else {
            this.setState({isRecommendOpen: false});
        }
    },
    handleSearch: function(e) {
        e.preventDefault();
        this.setState({isRecommendOpen: false});
        this.props.onSearch({word: this.state.word.trim()});
    },
    handleWordSelect: function(e) {
        e.preventDefault();
        this.setState({word: e.target.innerHTML, isRecommendOpen: false});
        this.props.onSearch({word: e.target.innerHTML});
    },
    render: function() {
        var Button;
        if (!this.props.searching) {
            Button = SearchButton;
        } else {
            Button = LoadingButton;
        }
        return (
            <form className="searchForm" onSubmit={this.handleSearch} style={{marginBottom: '10px'}}>
            <div className="input-group">
            <input type="search"
            className="form-control"
            placeholder="Search for..."
            value={this.state.word}
            onChange={this.handleWordChange} />
            <span className="input-group-btn">
            <Button onSearch={this.handleSearch} />
            </span>
            </div>
            <DropdownList
            isOpen={this.state.isRecommendOpen}
            recommendWords={this.state.recommendWords}
            onWordSelect={this.handleWordSelect}
            selectedNum={this.state.selectedNum}/>
            </form>
        );
    }
});

var AddModalButton = React.createClass({
    render: function() {
        var targetAttr = '#' + this.props.modalID;
        return (
            <button type="button" className="btn btn-danger"
                    data-toggle="modal"
                    data-target={targetAttr}>
                Add a word
            </button>
        );
    }
});

var AddModal = React.createClass({
    getInitialState: function() {
        return {
            word: "",
            part_of_speech: "",
            explanation: "",
            sentence: "",
            translation: "",
            addingDone: false
        };
    },
    handleWordChange: function(e) {
        this.setState({word: e.target.value});
    },
    handlePartOfSpeechChange: function(e) {
        this.setState({part_of_speech: e.target.value});
    },
    handleExplanationChange: function(e) {
        this.setState({explanation: e.target.value});
    },
    handleSentenceChange: function(e) {
        this.setState({sentence: e.target.value});
    },
    handleTranslationChange: function(e) {
        this.setState({translation: e.target.value});
    },
    handleAddClick: function(e) {
        var data = {
            word: this.state.word.trim(),
            meanings: [
                {
                    part_of_speech: this.state.part_of_speech.trim(),
                    explanation: this.state.explanation.trim()
                }
            ],
            examples: [
                {
                    sentence: this.state.sentence.trim(),
                    translation: this.state.translation.trim()
                }
            ]
        };
        $.ajax({
            url: '/api/add',
            dataType: 'json',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(data),
            success: function(data) {
                this.setState({addingDone: true})
            }.bind(this),
            error: function(xhr, status, err) {
                console.error('/api/add', status. err.toString());
            }.bind(this)
        });
    },
    handleCloseClick: function(e) {
        this.setState({
            word: "",
            part_of_speech: "",
            explanation: "",
            sentence: "",
            translation: "",
            addingDone: false
        });
    },
    render: function() {
        var displayState = {display: this.state.addingDone ? 'block' : 'none'};
        return (
            <div className="modal fade" id={this.props.id} tabIndex="-1" role="dialog" aria-labelledby="AddWordModel">
            <div className="modal-dialog" role="document">
            <div className="modal-content">
            <div className="modal-header">
            <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <h4 className="modal-title" id="myModalLabel">Add a word</h4>
            </div>
            <div className="modal-body">
            <form className="form-horizontal">
            <fieldset>
            <h4>Word</h4>
            <div className="form-group">
            <div className="col-lg-10">
            <input type="text" className="form-control" id="inputWord" placeholder="Word" value={this.state.word} onChange={this.handleWordChange }/>
            </div>
            </div>
            <h4>Meanings</h4>
            <ul className="list-group">
            <li className="list-group-item">
            <div className="form-group">
            <label htmlFor="inputPassword" className="col-lg-2 control-label">Part-of-speech</label>
            <div className="col-lg-10">
            <input type="text" className="form-control" id="inputExample" placeholder="Part-of-speech" value={this.state.part_of_speech} onChange={this.handlePartOfSpeechChange}/>
            </div>
            </div>
            <div className="form-group">
            <label htmlFor="inputPassword" className="col-lg-2 control-label">Explanation</label>
            <div className="col-lg-10">
            <input type="text" className="form-control" id="inputExample" placeholder="Explanation" value={this.state.explanation} onChange={this.handleExplanationChange}/>
            </div>
            </div>
            </li>
            </ul>
            <h4>Examples</h4>
            <ul className="list-group">
            <li className="list-group-item">
            <div className="form-group">
            <label htmlFor="inputPassword" className="col-lg-2 control-label">Sentence</label>
            <div className="col-lg-10">
            <input type="text" className="form-control" id="inputExample" placeholder="Sentence" value={this.state.sentence} onChange={this.handleSentenceChange}/>
            </div>
            </div>
            <div className="form-group">
            <label htmlFor="inputPassword" className="col-lg-2 control-label">Translation</label>
            <div className="col-lg-10">
            <input type="text" className="form-control" id="inputExample" placeholder="Translation" value={this.state.translation} onChange={this.handleTranslationChange }/>
            </div>
            </div>
            </li>
            </ul>
            </fieldset>
            </form>
            </div>
            <div className="modal-footer">
            <p className="text-success" style={displayState}><span className="glyphicon glyphicon-ok" aria-hidden="true"></span> Added!</p>
            <button type="button" className="btn btn-default" data-dismiss="modal" onClick={this.handleCloseClick}>Close</button>
            <button type="button" className="btn btn-primary" onClick={this.handleAddClick}>Add</button>
            </div>
            </div>
            </div>
            </div>
        );
    }
});

var Dictionary = React.createClass({
    getInitialState: function() {
        return {item: null, searching: false};
    },
    handleSearch: function(data) {
        // Get item by word from /api/find
        this.setState({searching: true});
        $.ajax({
            url: '/api/find',
            dataType: 'json',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(data),
            success: function(data) {
                this.setState({item: data.item, searching: false})
            }.bind(this),
            error: function(xhr, status, err) {
                console.error('/api/find', status. err.toString());
            }.bind(this)
        });
    },
    render: function() {
        return (
            <div className="container">
            <h1>Reactive English Chinese Dictionary</h1>
            <div className="row">
            <div className="col-xs-12 col-sm-6 col-md-4">
            <SearchInput searching={this.state.searching} onSearch={this.handleSearch}/>
            </div>
            </div>
            <div className="row">
            <div className="col-xs-12">
            <SearchResult item={this.state.item} />
            </div>
            </div>
            <AddModalButton modalID="add-modal"/>
            <AddModal id="add-modal"/>
            </div>
        );
    }
});

ReactDOM.render(
    <Dictionary />,
    document.getElementById('content')
);
