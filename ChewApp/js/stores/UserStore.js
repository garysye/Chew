'use strict';

var AppDispatcher = require('../dispatchers/AppDispatcher');
var EventEmitter = require('events').EventEmitter;
var FoodConstants = require('../constants/FoodConstants');
var assign = require('object-assign');

var CHANGE_EVENT = 'userChange';

var _currentAccount = {};
var _currentToken = {};

function populate (account, token) {
  _currentAccount  = account;
  _currentToken = token;
  console.log(_currentAccount);
}

function update (id, updates) {
  if (_currentAccount.id === id) {
    _currentAccount = assign({}, _currentAccount, updates);
  }
  console.log(_currentAccount);
}

function destroy () {
  _currentAccount = {};
}

var UserStore = assign({}, EventEmitter.prototype, {

  getAccount: function () {
    return _currentAccount;
  },

  getToken: function () {
    return _currentToken;
  },

  emitChange: function () {
    this.emit(CHANGE_EVENT);
  },

  addChangeListener: function (callback) {
    this.on(CHANGE_EVENT, callback);
  },

  removeChangeListener: function (callback) {
    this.removeListener(CHANGE_EVENT, callback);
  }
});

AppDispatcher.register(function(action) {
  var account, username, id;

  switch (action.actionType) {
    case FoodConstants.USER_SIGNIN:
      account = action.account;
      if (account.id) {
        populate(account);
        UserStore.emitChange();
      }
      break;

    case FoodConstants.USER_SIGNOUT:
      destroy();
      UserStore.emitChange();

      break;

    case FoodConstants.USER_UPDATE:
      id = action.account_id;
      if (id) {
        update(id, action.updates);
        UserStore.emitChange();
      }
      break;

    default:
  }
});

module.exports = UserStore;
