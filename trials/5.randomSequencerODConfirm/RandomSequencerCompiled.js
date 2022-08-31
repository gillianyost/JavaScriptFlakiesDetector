"use strict";

function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;

var _test = _interopRequireDefault(require("./test.json"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

function _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = _getPrototypeOf(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = _getPrototypeOf(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return _possibleConstructorReturn(this, result); }; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } else if (call !== void 0) { throw new TypeError("Derived constructors may only return object or undefined"); } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _isNativeReflectConstruct() { if (typeof Reflect === "undefined" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === "function") return true; try { Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {})); return true; } catch (e) { return false; } }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

var TestSequencer = require('@jest/test-sequencer')["default"];

var seedrandom = require('seedrandom');

var fs = require('fs');

var CustomSequencer = /*#__PURE__*/function (_TestSequencer) {
  _inherits(CustomSequencer, _TestSequencer);

  var _super = _createSuper(CustomSequencer);

  function CustomSequencer() {
    _classCallCheck(this, CustomSequencer);

    return _super.apply(this, arguments);
  }

  _createClass(CustomSequencer, [{
    key: "sort",
    value: function sort(tests) {
      tests.sort(function (testA, testB) {
        return testA.path > testB.path ? 1 : -1;
      });
      var lastTest = _test["default"][_test["default"].length - 1];
      var generator;

      if (lastTest.flakyTestDetected) {
        console.log("Seed: ", lastTest.seed.toString());
        generator = seedrandom(lastTest.seed.toString());
        var newTest = {
          seed: lastTest.seed
        };

        _test["default"].push(newTest);

        var newData = JSON.stringify(_test["default"]);
        fs.writeFile('test.json', newData, function (err) {});
      } else {
        var newSeed = Math.random();
        console.log("Seed: ", newSeed);
        generator = seedrandom(newSeed.toString());
        var _newTest = {
          seed: newSeed
        };

        _test["default"].push(_newTest);

        var _newData = JSON.stringify(_test["default"]);

        fs.writeFile('test.json', _newData, function (err) {});
      }

      for (var i = tests.length - 1; i > 0; i--) {
        var value = generator();
        console.log("Value: ", value);
        var j = Math.floor(value * (i + 1));
        var temp = tests[i];
        tests[i] = tests[j];
        tests[j] = temp;
      } // Durstenfeld Shuffle - updated due to the Fisher-Yates not working correctly for 2 test suites


      return tests;
    }
  }]);

  return CustomSequencer;
}(TestSequencer);

var _default = CustomSequencer;
exports["default"] = _default;
