module.exports = {
  root: true,
  parser: 'babel-eslint',
  extends: 'airbnb-base',
  plugins: [],
  parserOptions: {
    ecmaVersion: 6,
    sourceType: 'module',
  },
  env: {
    es6: true,
    node: true,
    browser: true,
  },
  'globals': {
    'FB': true,
    'twttr': true,
    'gapi': true,
    '$': true,
  },
  'rules': {
    'camelcase': ['warn'],
    'no-unused-vars': ['warn'],
    'no-console': ['off'],
    'max-len': ['off'],
    'semi': ['error', 'never'],
    'arrow-body-style': ['off'],
    'indent': [1, 4, { 'SwitchCase': 1 }],
    'import/extensions': ['off'],
    'import/no-extraneous-dependencies': ['off'],
    'no-tabs': ['off'],
    'no-return-assign': ['off'],
    'no-unused-expressions': ['off'],
    'import/no-named-default': ['off']
  },
  settings: {
    'import/resolver': {
      webpack: {
        config: './webpack/config.test.babel.js'
      }
    }
  }
}
