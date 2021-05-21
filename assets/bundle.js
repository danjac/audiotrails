(() => {
  var __create = Object.create,
    __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __getProtoOf = Object.getPrototypeOf,
    __hasOwnProp = Object.prototype.hasOwnProperty;
  var __markAsModule = (target) => __defProp(target, '__esModule', { value: !0 });
  var __commonJS = (cb, mod) =>
    function () {
      return (
        mod || (0, cb[Object.keys(cb)[0]])((mod = { exports: {} }).exports, mod),
        mod.exports
      );
    };
  var __reExport = (target, module2, desc) => {
      if ((module2 && typeof module2 == 'object') || typeof module2 == 'function')
        for (let key of __getOwnPropNames(module2))
          !__hasOwnProp.call(target, key) &&
            key !== 'default' &&
            __defProp(target, key, {
              get: () => module2[key],
              enumerable: !(desc = __getOwnPropDesc(module2, key)) || desc.enumerable,
            });
      return target;
    },
    __toModule = (module2) =>
      __reExport(
        __markAsModule(
          __defProp(
            module2 != null ? __create(__getProtoOf(module2)) : {},
            'default',
            module2 && module2.__esModule && 'default' in module2
              ? { get: () => module2.default, enumerable: !0 }
              : { value: module2, enumerable: !0 }
          )
        ),
        module2
      );
  var require_alpine = __commonJS({
    'node_modules/alpinejs/dist/alpine.js'(exports2, module2) {
      (function (global, factory) {
        typeof exports2 == 'object' && typeof module2 != 'undefined'
          ? (module2.exports = factory())
          : typeof define == 'function' && define.amd
          ? define(factory)
          : ((global = global || self), (global.Alpine = factory()));
      })(exports2, function () {
        'use strict';
        function _defineProperty2(obj, key, value) {
          return (
            key in obj
              ? Object.defineProperty(obj, key, {
                  value,
                  enumerable: !0,
                  configurable: !0,
                  writable: !0,
                })
              : (obj[key] = value),
            obj
          );
        }
        function ownKeys(object, enumerableOnly) {
          var keys = Object.keys(object);
          if (Object.getOwnPropertySymbols) {
            var symbols = Object.getOwnPropertySymbols(object);
            enumerableOnly &&
              (symbols = symbols.filter(function (sym) {
                return Object.getOwnPropertyDescriptor(object, sym).enumerable;
              })),
              keys.push.apply(keys, symbols);
          }
          return keys;
        }
        function _objectSpread2(target) {
          for (var i = 1; i < arguments.length; i++) {
            var source = arguments[i] != null ? arguments[i] : {};
            i % 2
              ? ownKeys(Object(source), !0).forEach(function (key) {
                  _defineProperty2(target, key, source[key]);
                })
              : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(
                  target,
                  Object.getOwnPropertyDescriptors(source)
                )
              : ownKeys(Object(source)).forEach(function (key) {
                  Object.defineProperty(
                    target,
                    key,
                    Object.getOwnPropertyDescriptor(source, key)
                  );
                });
          }
          return target;
        }
        function domReady() {
          return new Promise((resolve) => {
            document.readyState == 'loading'
              ? document.addEventListener('DOMContentLoaded', resolve)
              : resolve();
          });
        }
        function arrayUnique(array) {
          return Array.from(new Set(array));
        }
        function isTesting() {
          return (
            navigator.userAgent.includes('Node.js') ||
            navigator.userAgent.includes('jsdom')
          );
        }
        function checkedAttrLooseCompare(valueA, valueB) {
          return valueA == valueB;
        }
        function warnIfMalformedTemplate(el, directive) {
          el.tagName.toLowerCase() !== 'template'
            ? console.warn(
                `Alpine: [${directive}] directive should only be added to <template> tags. See https://github.com/alpinejs/alpine#${directive}`
              )
            : el.content.childElementCount !== 1 &&
              console.warn(
                `Alpine: <template> tag with [${directive}] encountered with an unexpected number of root elements. Make sure <template> has a single root element. `
              );
        }
        function kebabCase(subject) {
          return subject
            .replace(/([a-z])([A-Z])/g, '$1-$2')
            .replace(/[_\s]/, '-')
            .toLowerCase();
        }
        function camelCase(subject) {
          return subject
            .toLowerCase()
            .replace(/-(\w)/g, (match, char) => char.toUpperCase());
        }
        function walk(el, callback) {
          if (callback(el) === !1) return;
          let node = el.firstElementChild;
          for (; node; ) walk(node, callback), (node = node.nextElementSibling);
        }
        function debounce(func, wait) {
          var timeout;
          return function () {
            var context = this,
              args = arguments,
              later = function () {
                (timeout = null), func.apply(context, args);
              };
            clearTimeout(timeout), (timeout = setTimeout(later, wait));
          };
        }
        let handleError = (el, expression, error) => {
          if (
            (console.warn(
              `Alpine Error: "${error}"

Expression: "${expression}"
Element:`,
              el
            ),
            !isTesting())
          )
            throw (Object.assign(error, { el, expression }), error);
        };
        function tryCatch(cb, { el, expression }) {
          try {
            let value = cb();
            return value instanceof Promise
              ? value.catch((e) => handleError(el, expression, e))
              : value;
          } catch (e) {
            handleError(el, expression, e);
          }
        }
        function saferEval(
          el,
          expression,
          dataContext,
          additionalHelperVariables = {}
        ) {
          return tryCatch(
            () =>
              typeof expression == 'function'
                ? expression.call(dataContext)
                : new Function(
                    ['$data', ...Object.keys(additionalHelperVariables)],
                    `var __alpine_result; with($data) { __alpine_result = ${expression} }; return __alpine_result`
                  )(dataContext, ...Object.values(additionalHelperVariables)),
            { el, expression }
          );
        }
        function saferEvalNoReturn(
          el,
          expression,
          dataContext,
          additionalHelperVariables = {}
        ) {
          return tryCatch(
            () => {
              if (typeof expression == 'function')
                return Promise.resolve(
                  expression.call(dataContext, additionalHelperVariables.$event)
                );
              let AsyncFunction = Function;
              if (
                ((AsyncFunction = Object.getPrototypeOf(async function () {})
                  .constructor),
                Object.keys(dataContext).includes(expression))
              ) {
                let methodReference = new Function(
                  ['dataContext', ...Object.keys(additionalHelperVariables)],
                  `with(dataContext) { return ${expression} }`
                )(dataContext, ...Object.values(additionalHelperVariables));
                return typeof methodReference == 'function'
                  ? Promise.resolve(
                      methodReference.call(
                        dataContext,
                        additionalHelperVariables.$event
                      )
                    )
                  : Promise.resolve();
              }
              return Promise.resolve(
                new AsyncFunction(
                  ['dataContext', ...Object.keys(additionalHelperVariables)],
                  `with(dataContext) { ${expression} }`
                )(dataContext, ...Object.values(additionalHelperVariables))
              );
            },
            { el, expression }
          );
        }
        let xAttrRE = /^x-(on|bind|data|text|html|model|if|for|show|cloak|transition|ref|spread)\b/;
        function isXAttr(attr) {
          let name = replaceAtAndColonWithStandardSyntax(attr.name);
          return xAttrRE.test(name);
        }
        function getXAttrs(el, component, type) {
          let directives = Array.from(el.attributes)
              .filter(isXAttr)
              .map(parseHtmlAttribute),
            spreadDirective = directives.filter(
              (directive) => directive.type === 'spread'
            )[0];
          if (spreadDirective) {
            let spreadObject = saferEval(
              el,
              spreadDirective.expression,
              component.$data
            );
            directives = directives.concat(
              Object.entries(spreadObject).map(([name, value]) =>
                parseHtmlAttribute({ name, value })
              )
            );
          }
          return type
            ? directives.filter((i) => i.type === type)
            : sortDirectives(directives);
        }
        function sortDirectives(directives) {
          let directiveOrder = ['bind', 'model', 'show', 'catch-all'];
          return directives.sort((a, b) => {
            let typeA = directiveOrder.indexOf(a.type) === -1 ? 'catch-all' : a.type,
              typeB = directiveOrder.indexOf(b.type) === -1 ? 'catch-all' : b.type;
            return directiveOrder.indexOf(typeA) - directiveOrder.indexOf(typeB);
          });
        }
        function parseHtmlAttribute({ name, value }) {
          let normalizedName = replaceAtAndColonWithStandardSyntax(name),
            typeMatch = normalizedName.match(xAttrRE),
            valueMatch = normalizedName.match(/:([a-zA-Z0-9\-:]+)/),
            modifiers = normalizedName.match(/\.[^.\]]+(?=[^\]]*$)/g) || [];
          return {
            type: typeMatch ? typeMatch[1] : null,
            value: valueMatch ? valueMatch[1] : null,
            modifiers: modifiers.map((i) => i.replace('.', '')),
            expression: value,
          };
        }
        function isBooleanAttr(attrName) {
          return [
            'disabled',
            'checked',
            'required',
            'readonly',
            'hidden',
            'open',
            'selected',
            'autofocus',
            'itemscope',
            'multiple',
            'novalidate',
            'allowfullscreen',
            'allowpaymentrequest',
            'formnovalidate',
            'autoplay',
            'controls',
            'loop',
            'muted',
            'playsinline',
            'default',
            'ismap',
            'reversed',
            'async',
            'defer',
            'nomodule',
          ].includes(attrName);
        }
        function replaceAtAndColonWithStandardSyntax(name) {
          return name.startsWith('@')
            ? name.replace('@', 'x-on:')
            : name.startsWith(':')
            ? name.replace(':', 'x-bind:')
            : name;
        }
        function convertClassStringToArray(classList, filterFn = Boolean) {
          return classList.split(' ').filter(filterFn);
        }
        let TRANSITION_TYPE_IN = 'in',
          TRANSITION_TYPE_OUT = 'out',
          TRANSITION_CANCELLED = 'cancelled';
        function transitionIn(el, show, reject, component, forceSkip = !1) {
          if (forceSkip) return show();
          if (el.__x_transition && el.__x_transition.type === TRANSITION_TYPE_IN)
            return;
          let attrs = getXAttrs(el, component, 'transition'),
            showAttr = getXAttrs(el, component, 'show')[0];
          if (showAttr && showAttr.modifiers.includes('transition')) {
            let modifiers = showAttr.modifiers;
            if (modifiers.includes('out') && !modifiers.includes('in')) return show();
            (modifiers =
              modifiers.includes('in') && modifiers.includes('out')
                ? modifiers.filter((i, index2) => index2 < modifiers.indexOf('out'))
                : modifiers),
              transitionHelperIn(el, modifiers, show, reject);
          } else attrs.some((attr) => ['enter', 'enter-start', 'enter-end'].includes(attr.value)) ? transitionClassesIn(el, component, attrs, show, reject) : show();
        }
        function transitionOut(el, hide, reject, component, forceSkip = !1) {
          if (forceSkip) return hide();
          if (el.__x_transition && el.__x_transition.type === TRANSITION_TYPE_OUT)
            return;
          let attrs = getXAttrs(el, component, 'transition'),
            showAttr = getXAttrs(el, component, 'show')[0];
          if (showAttr && showAttr.modifiers.includes('transition')) {
            let modifiers = showAttr.modifiers;
            if (modifiers.includes('in') && !modifiers.includes('out')) return hide();
            let settingBothSidesOfTransition =
              modifiers.includes('in') && modifiers.includes('out');
            (modifiers = settingBothSidesOfTransition
              ? modifiers.filter((i, index2) => index2 > modifiers.indexOf('out'))
              : modifiers),
              transitionHelperOut(
                el,
                modifiers,
                settingBothSidesOfTransition,
                hide,
                reject
              );
          } else attrs.some((attr) => ['leave', 'leave-start', 'leave-end'].includes(attr.value)) ? transitionClassesOut(el, component, attrs, hide, reject) : hide();
        }
        function transitionHelperIn(el, modifiers, showCallback, reject) {
          let styleValues = {
            duration: modifierValue(modifiers, 'duration', 150),
            origin: modifierValue(modifiers, 'origin', 'center'),
            first: { opacity: 0, scale: modifierValue(modifiers, 'scale', 95) },
            second: { opacity: 1, scale: 100 },
          };
          transitionHelper(
            el,
            modifiers,
            showCallback,
            () => {},
            reject,
            styleValues,
            TRANSITION_TYPE_IN
          );
        }
        function transitionHelperOut(
          el,
          modifiers,
          settingBothSidesOfTransition,
          hideCallback,
          reject
        ) {
          let styleValues = {
            duration: settingBothSidesOfTransition
              ? modifierValue(modifiers, 'duration', 150)
              : modifierValue(modifiers, 'duration', 150) / 2,
            origin: modifierValue(modifiers, 'origin', 'center'),
            first: { opacity: 1, scale: 100 },
            second: { opacity: 0, scale: modifierValue(modifiers, 'scale', 95) },
          };
          transitionHelper(
            el,
            modifiers,
            () => {},
            hideCallback,
            reject,
            styleValues,
            TRANSITION_TYPE_OUT
          );
        }
        function modifierValue(modifiers, key, fallback) {
          if (modifiers.indexOf(key) === -1) return fallback;
          let rawValue = modifiers[modifiers.indexOf(key) + 1];
          if (!rawValue || (key === 'scale' && !isNumeric(rawValue))) return fallback;
          if (key === 'duration') {
            let match = rawValue.match(/([0-9]+)ms/);
            if (match) return match[1];
          }
          return key === 'origin' &&
            ['top', 'right', 'left', 'center', 'bottom'].includes(
              modifiers[modifiers.indexOf(key) + 2]
            )
            ? [rawValue, modifiers[modifiers.indexOf(key) + 2]].join(' ')
            : rawValue;
        }
        function transitionHelper(
          el,
          modifiers,
          hook1,
          hook2,
          reject,
          styleValues,
          type
        ) {
          el.__x_transition && el.__x_transition.cancel && el.__x_transition.cancel();
          let opacityCache = el.style.opacity,
            transformCache = el.style.transform,
            transformOriginCache = el.style.transformOrigin,
            noModifiers =
              !modifiers.includes('opacity') && !modifiers.includes('scale'),
            transitionOpacity = noModifiers || modifiers.includes('opacity'),
            transitionScale = noModifiers || modifiers.includes('scale');
          transition(
            el,
            {
              start() {
                transitionOpacity && (el.style.opacity = styleValues.first.opacity),
                  transitionScale &&
                    (el.style.transform = `scale(${styleValues.first.scale / 100})`);
              },
              during() {
                transitionScale && (el.style.transformOrigin = styleValues.origin),
                  (el.style.transitionProperty = [
                    transitionOpacity ? 'opacity' : '',
                    transitionScale ? 'transform' : '',
                  ]
                    .join(' ')
                    .trim()),
                  (el.style.transitionDuration = `${styleValues.duration / 1e3}s`),
                  (el.style.transitionTimingFunction =
                    'cubic-bezier(0.4, 0.0, 0.2, 1)');
              },
              show() {
                hook1();
              },
              end() {
                transitionOpacity && (el.style.opacity = styleValues.second.opacity),
                  transitionScale &&
                    (el.style.transform = `scale(${styleValues.second.scale / 100})`);
              },
              hide() {
                hook2();
              },
              cleanup() {
                transitionOpacity && (el.style.opacity = opacityCache),
                  transitionScale && (el.style.transform = transformCache),
                  transitionScale && (el.style.transformOrigin = transformOriginCache),
                  (el.style.transitionProperty = null),
                  (el.style.transitionDuration = null),
                  (el.style.transitionTimingFunction = null);
              },
            },
            type,
            reject
          );
        }
        let ensureStringExpression = (expression, el, component) =>
          typeof expression == 'function'
            ? component.evaluateReturnExpression(el, expression)
            : expression;
        function transitionClassesIn(el, component, directives, showCallback, reject) {
          let enter = convertClassStringToArray(
              ensureStringExpression(
                (directives.find((i) => i.value === 'enter') || { expression: '' })
                  .expression,
                el,
                component
              )
            ),
            enterStart = convertClassStringToArray(
              ensureStringExpression(
                (
                  directives.find((i) => i.value === 'enter-start') || {
                    expression: '',
                  }
                ).expression,
                el,
                component
              )
            ),
            enterEnd = convertClassStringToArray(
              ensureStringExpression(
                (directives.find((i) => i.value === 'enter-end') || { expression: '' })
                  .expression,
                el,
                component
              )
            );
          transitionClasses(
            el,
            enter,
            enterStart,
            enterEnd,
            showCallback,
            () => {},
            TRANSITION_TYPE_IN,
            reject
          );
        }
        function transitionClassesOut(el, component, directives, hideCallback, reject) {
          let leave = convertClassStringToArray(
              ensureStringExpression(
                (directives.find((i) => i.value === 'leave') || { expression: '' })
                  .expression,
                el,
                component
              )
            ),
            leaveStart = convertClassStringToArray(
              ensureStringExpression(
                (
                  directives.find((i) => i.value === 'leave-start') || {
                    expression: '',
                  }
                ).expression,
                el,
                component
              )
            ),
            leaveEnd = convertClassStringToArray(
              ensureStringExpression(
                (directives.find((i) => i.value === 'leave-end') || { expression: '' })
                  .expression,
                el,
                component
              )
            );
          transitionClasses(
            el,
            leave,
            leaveStart,
            leaveEnd,
            () => {},
            hideCallback,
            TRANSITION_TYPE_OUT,
            reject
          );
        }
        function transitionClasses(
          el,
          classesDuring,
          classesStart,
          classesEnd,
          hook1,
          hook2,
          type,
          reject
        ) {
          el.__x_transition && el.__x_transition.cancel && el.__x_transition.cancel();
          let originalClasses = el.__x_original_classes || [];
          transition(
            el,
            {
              start() {
                el.classList.add(...classesStart);
              },
              during() {
                el.classList.add(...classesDuring);
              },
              show() {
                hook1();
              },
              end() {
                el.classList.remove(
                  ...classesStart.filter((i) => !originalClasses.includes(i))
                ),
                  el.classList.add(...classesEnd);
              },
              hide() {
                hook2();
              },
              cleanup() {
                el.classList.remove(
                  ...classesDuring.filter((i) => !originalClasses.includes(i))
                ),
                  el.classList.remove(
                    ...classesEnd.filter((i) => !originalClasses.includes(i))
                  );
              },
            },
            type,
            reject
          );
        }
        function transition(el, stages, type, reject) {
          let finish = once(() => {
            stages.hide(), el.isConnected && stages.cleanup(), delete el.__x_transition;
          });
          (el.__x_transition = {
            type,
            cancel: once(() => {
              reject(TRANSITION_CANCELLED), finish();
            }),
            finish,
            nextFrame: null,
          }),
            stages.start(),
            stages.during(),
            (el.__x_transition.nextFrame = requestAnimationFrame(() => {
              let duration =
                Number(
                  getComputedStyle(el)
                    .transitionDuration.replace(/,.*/, '')
                    .replace('s', '')
                ) * 1e3;
              duration === 0 &&
                (duration =
                  Number(getComputedStyle(el).animationDuration.replace('s', '')) *
                  1e3),
                stages.show(),
                (el.__x_transition.nextFrame = requestAnimationFrame(() => {
                  stages.end(), setTimeout(el.__x_transition.finish, duration);
                }));
            }));
        }
        function isNumeric(subject) {
          return !Array.isArray(subject) && !isNaN(subject);
        }
        function once(callback) {
          let called = !1;
          return function () {
            called || ((called = !0), callback.apply(this, arguments));
          };
        }
        function handleForDirective(
          component,
          templateEl,
          expression,
          initialUpdate,
          extraVars
        ) {
          warnIfMalformedTemplate(templateEl, 'x-for');
          let iteratorNames =
              typeof expression == 'function'
                ? parseForExpression(
                    component.evaluateReturnExpression(templateEl, expression)
                  )
                : parseForExpression(expression),
            items = evaluateItemsAndReturnEmptyIfXIfIsPresentAndFalseOnElement(
              component,
              templateEl,
              iteratorNames,
              extraVars
            ),
            currentEl = templateEl;
          items.forEach((item, index2) => {
            let iterationScopeVariables = getIterationScopeVariables(
                iteratorNames,
                item,
                index2,
                items,
                extraVars()
              ),
              currentKey = generateKeyForIteration(
                component,
                templateEl,
                index2,
                iterationScopeVariables
              ),
              nextEl2 = lookAheadForMatchingKeyedElementAndMoveItIfFound(
                currentEl.nextElementSibling,
                currentKey
              );
            nextEl2
              ? (delete nextEl2.__x_for_key,
                (nextEl2.__x_for = iterationScopeVariables),
                component.updateElements(nextEl2, () => nextEl2.__x_for))
              : ((nextEl2 = addElementInLoopAfterCurrentEl(templateEl, currentEl)),
                transitionIn(
                  nextEl2,
                  () => {},
                  () => {},
                  component,
                  initialUpdate
                ),
                (nextEl2.__x_for = iterationScopeVariables),
                component.initializeElements(nextEl2, () => nextEl2.__x_for)),
              (currentEl = nextEl2),
              (currentEl.__x_for_key = currentKey);
          }),
            removeAnyLeftOverElementsFromPreviousUpdate(currentEl, component);
        }
        function parseForExpression(expression) {
          let forIteratorRE = /,([^,\}\]]*)(?:,([^,\}\]]*))?$/,
            stripParensRE = /^\(|\)$/g,
            forAliasRE = /([\s\S]*?)\s+(?:in|of)\s+([\s\S]*)/,
            inMatch = String(expression).match(forAliasRE);
          if (!inMatch) return;
          let res = {};
          res.items = inMatch[2].trim();
          let item = inMatch[1].trim().replace(stripParensRE, ''),
            iteratorMatch = item.match(forIteratorRE);
          return (
            iteratorMatch
              ? ((res.item = item.replace(forIteratorRE, '').trim()),
                (res.index = iteratorMatch[1].trim()),
                iteratorMatch[2] && (res.collection = iteratorMatch[2].trim()))
              : (res.item = item),
            res
          );
        }
        function getIterationScopeVariables(
          iteratorNames,
          item,
          index2,
          items,
          extraVars
        ) {
          let scopeVariables = extraVars ? _objectSpread2({}, extraVars) : {};
          return (
            (scopeVariables[iteratorNames.item] = item),
            iteratorNames.index && (scopeVariables[iteratorNames.index] = index2),
            iteratorNames.collection &&
              (scopeVariables[iteratorNames.collection] = items),
            scopeVariables
          );
        }
        function generateKeyForIteration(
          component,
          el,
          index2,
          iterationScopeVariables
        ) {
          let bindKeyAttribute = getXAttrs(el, component, 'bind').filter(
            (attr) => attr.value === 'key'
          )[0];
          return bindKeyAttribute
            ? component.evaluateReturnExpression(
                el,
                bindKeyAttribute.expression,
                () => iterationScopeVariables
              )
            : index2;
        }
        function evaluateItemsAndReturnEmptyIfXIfIsPresentAndFalseOnElement(
          component,
          el,
          iteratorNames,
          extraVars
        ) {
          let ifAttribute = getXAttrs(el, component, 'if')[0];
          if (
            ifAttribute &&
            !component.evaluateReturnExpression(el, ifAttribute.expression)
          )
            return [];
          let items = component.evaluateReturnExpression(
            el,
            iteratorNames.items,
            extraVars
          );
          return (
            isNumeric(items) &&
              items >= 0 &&
              (items = Array.from(Array(items).keys(), (i) => i + 1)),
            items
          );
        }
        function addElementInLoopAfterCurrentEl(templateEl, currentEl) {
          let clone2 = document.importNode(templateEl.content, !0);
          return (
            currentEl.parentElement.insertBefore(clone2, currentEl.nextElementSibling),
            currentEl.nextElementSibling
          );
        }
        function lookAheadForMatchingKeyedElementAndMoveItIfFound(nextEl2, currentKey) {
          if (!nextEl2 || nextEl2.__x_for_key === void 0) return;
          if (nextEl2.__x_for_key === currentKey) return nextEl2;
          let tmpNextEl = nextEl2;
          for (; tmpNextEl; ) {
            if (tmpNextEl.__x_for_key === currentKey)
              return tmpNextEl.parentElement.insertBefore(tmpNextEl, nextEl2);
            tmpNextEl =
              tmpNextEl.nextElementSibling &&
              tmpNextEl.nextElementSibling.__x_for_key !== void 0
                ? tmpNextEl.nextElementSibling
                : !1;
          }
        }
        function removeAnyLeftOverElementsFromPreviousUpdate(currentEl, component) {
          for (
            var nextElementFromOldLoop =
              currentEl.nextElementSibling &&
              currentEl.nextElementSibling.__x_for_key !== void 0
                ? currentEl.nextElementSibling
                : !1;
            nextElementFromOldLoop;

          ) {
            let nextElementFromOldLoopImmutable = nextElementFromOldLoop,
              nextSibling = nextElementFromOldLoop.nextElementSibling;
            transitionOut(
              nextElementFromOldLoop,
              () => {
                nextElementFromOldLoopImmutable.remove();
              },
              () => {},
              component
            ),
              (nextElementFromOldLoop =
                nextSibling && nextSibling.__x_for_key !== void 0 ? nextSibling : !1);
          }
        }
        function handleAttributeBindingDirective(
          component,
          el,
          attrName,
          expression,
          extraVars,
          attrType,
          modifiers
        ) {
          var value = component.evaluateReturnExpression(el, expression, extraVars);
          if (attrName === 'value') {
            if (
              Alpine.ignoreFocusedForValueBinding &&
              document.activeElement.isSameNode(el)
            )
              return;
            if (
              (value === void 0 && String(expression).match(/\./) && (value = ''),
              el.type === 'radio')
            )
              el.attributes.value === void 0 && attrType === 'bind'
                ? (el.value = value)
                : attrType !== 'bind' &&
                  (el.checked = checkedAttrLooseCompare(el.value, value));
            else if (el.type === 'checkbox')
              typeof value != 'boolean' &&
              ![null, void 0].includes(value) &&
              attrType === 'bind'
                ? (el.value = String(value))
                : attrType !== 'bind' &&
                  (Array.isArray(value)
                    ? (el.checked = value.some((val) =>
                        checkedAttrLooseCompare(val, el.value)
                      ))
                    : (el.checked = !!value));
            else if (el.tagName === 'SELECT') updateSelect(el, value);
            else {
              if (el.value === value) return;
              el.value = value;
            }
          } else if (attrName === 'class')
            if (Array.isArray(value)) {
              let originalClasses = el.__x_original_classes || [];
              el.setAttribute(
                'class',
                arrayUnique(originalClasses.concat(value)).join(' ')
              );
            } else if (typeof value == 'object')
              Object.keys(value)
                .sort((a, b) => value[a] - value[b])
                .forEach((classNames) => {
                  value[classNames]
                    ? convertClassStringToArray(classNames).forEach((className) =>
                        el.classList.add(className)
                      )
                    : convertClassStringToArray(classNames).forEach((className) =>
                        el.classList.remove(className)
                      );
                });
            else {
              let originalClasses = el.__x_original_classes || [],
                newClasses = value ? convertClassStringToArray(value) : [];
              el.setAttribute(
                'class',
                arrayUnique(originalClasses.concat(newClasses)).join(' ')
              );
            }
          else
            (attrName = modifiers.includes('camel') ? camelCase(attrName) : attrName),
              [null, void 0, !1].includes(value)
                ? el.removeAttribute(attrName)
                : isBooleanAttr(attrName)
                ? setIfChanged(el, attrName, attrName)
                : setIfChanged(el, attrName, value);
        }
        function setIfChanged(el, attrName, value) {
          el.getAttribute(attrName) != value && el.setAttribute(attrName, value);
        }
        function updateSelect(el, value) {
          let arrayWrappedValue = [].concat(value).map((value2) => value2 + '');
          Array.from(el.options).forEach((option2) => {
            option2.selected = arrayWrappedValue.includes(
              option2.value || option2.text
            );
          });
        }
        function handleTextDirective(el, output, expression) {
          output === void 0 && String(expression).match(/\./) && (output = ''),
            (el.textContent = output);
        }
        function handleHtmlDirective(component, el, expression, extraVars) {
          el.innerHTML = component.evaluateReturnExpression(el, expression, extraVars);
        }
        function handleShowDirective(
          component,
          el,
          value,
          modifiers,
          initialUpdate = !1
        ) {
          let hide = () => {
              (el.style.display = 'none'), (el.__x_is_shown = !1);
            },
            show = () => {
              el.style.length === 1 && el.style.display === 'none'
                ? el.removeAttribute('style')
                : el.style.removeProperty('display'),
                (el.__x_is_shown = !0);
            };
          if (initialUpdate === !0) {
            value ? show() : hide();
            return;
          }
          let handle = (resolve, reject) => {
            value
              ? ((el.style.display === 'none' || el.__x_transition) &&
                  transitionIn(
                    el,
                    () => {
                      show();
                    },
                    reject,
                    component
                  ),
                resolve(() => {}))
              : el.style.display !== 'none'
              ? transitionOut(
                  el,
                  () => {
                    resolve(() => {
                      hide();
                    });
                  },
                  reject,
                  component
                )
              : resolve(() => {});
          };
          if (modifiers.includes('immediate')) {
            handle(
              (finish) => finish(),
              () => {}
            );
            return;
          }
          component.showDirectiveLastElement &&
            !component.showDirectiveLastElement.contains(el) &&
            component.executeAndClearRemainingShowDirectiveStack(),
            component.showDirectiveStack.push(handle),
            (component.showDirectiveLastElement = el);
        }
        function handleIfDirective(
          component,
          el,
          expressionResult,
          initialUpdate,
          extraVars
        ) {
          warnIfMalformedTemplate(el, 'x-if');
          let elementHasAlreadyBeenAdded =
            el.nextElementSibling && el.nextElementSibling.__x_inserted_me === !0;
          if (expressionResult && (!elementHasAlreadyBeenAdded || el.__x_transition)) {
            let clone2 = document.importNode(el.content, !0);
            el.parentElement.insertBefore(clone2, el.nextElementSibling),
              transitionIn(
                el.nextElementSibling,
                () => {},
                () => {},
                component,
                initialUpdate
              ),
              component.initializeElements(el.nextElementSibling, extraVars),
              (el.nextElementSibling.__x_inserted_me = !0);
          } else
            !expressionResult &&
              elementHasAlreadyBeenAdded &&
              transitionOut(
                el.nextElementSibling,
                () => {
                  el.nextElementSibling.remove();
                },
                () => {},
                component,
                initialUpdate
              );
        }
        function registerListener(
          component,
          el,
          event,
          modifiers,
          expression,
          extraVars = {}
        ) {
          let options = { passive: modifiers.includes('passive') };
          modifiers.includes('camel') && (event = camelCase(event));
          let handler, listenerTarget;
          if (
            (modifiers.includes('away')
              ? ((listenerTarget = document),
                (handler = (e) => {
                  el.contains(e.target) ||
                    (el.offsetWidth < 1 && el.offsetHeight < 1) ||
                    (runListenerHandler(component, expression, e, extraVars),
                    modifiers.includes('once') &&
                      document.removeEventListener(event, handler, options));
                }))
              : ((listenerTarget = modifiers.includes('window')
                  ? window
                  : modifiers.includes('document')
                  ? document
                  : el),
                (handler = (e) => {
                  if (
                    (listenerTarget === window || listenerTarget === document) &&
                    !document.body.contains(el)
                  ) {
                    listenerTarget.removeEventListener(event, handler, options);
                    return;
                  }
                  (isKeyEvent(event) &&
                    isListeningForASpecificKeyThatHasntBeenPressed(e, modifiers)) ||
                    (modifiers.includes('prevent') && e.preventDefault(),
                    modifiers.includes('stop') && e.stopPropagation(),
                    (!modifiers.includes('self') || e.target === el) &&
                      runListenerHandler(component, expression, e, extraVars).then(
                        (value) => {
                          value === !1
                            ? e.preventDefault()
                            : modifiers.includes('once') &&
                              listenerTarget.removeEventListener(
                                event,
                                handler,
                                options
                              );
                        }
                      ));
                })),
            modifiers.includes('debounce'))
          ) {
            let nextModifier =
                modifiers[modifiers.indexOf('debounce') + 1] || 'invalid-wait',
              wait = isNumeric(nextModifier.split('ms')[0])
                ? Number(nextModifier.split('ms')[0])
                : 250;
            handler = debounce(handler, wait);
          }
          listenerTarget.addEventListener(event, handler, options);
        }
        function runListenerHandler(component, expression, e, extraVars) {
          return component.evaluateCommandExpression(e.target, expression, () =>
            _objectSpread2(_objectSpread2({}, extraVars()), {}, { $event: e })
          );
        }
        function isKeyEvent(event) {
          return ['keydown', 'keyup'].includes(event);
        }
        function isListeningForASpecificKeyThatHasntBeenPressed(e, modifiers) {
          let keyModifiers = modifiers.filter(
            (i) => !['window', 'document', 'prevent', 'stop'].includes(i)
          );
          if (keyModifiers.includes('debounce')) {
            let debounceIndex = keyModifiers.indexOf('debounce');
            keyModifiers.splice(
              debounceIndex,
              isNumeric(
                (keyModifiers[debounceIndex + 1] || 'invalid-wait').split('ms')[0]
              )
                ? 2
                : 1
            );
          }
          if (
            keyModifiers.length === 0 ||
            (keyModifiers.length === 1 && keyModifiers[0] === keyToModifier(e.key))
          )
            return !1;
          let selectedSystemKeyModifiers = [
            'ctrl',
            'shift',
            'alt',
            'meta',
            'cmd',
            'super',
          ].filter((modifier) => keyModifiers.includes(modifier));
          return (
            (keyModifiers = keyModifiers.filter(
              (i) => !selectedSystemKeyModifiers.includes(i)
            )),
            !(
              selectedSystemKeyModifiers.length > 0 &&
              selectedSystemKeyModifiers.filter(
                (modifier) => (
                  (modifier === 'cmd' || modifier === 'super') && (modifier = 'meta'),
                  e[`${modifier}Key`]
                )
              ).length === selectedSystemKeyModifiers.length &&
              keyModifiers[0] === keyToModifier(e.key)
            )
          );
        }
        function keyToModifier(key) {
          switch (key) {
            case '/':
              return 'slash';
            case ' ':
            case 'Spacebar':
              return 'space';
            default:
              return key && kebabCase(key);
          }
        }
        function registerModelListener(
          component,
          el,
          modifiers,
          expression,
          extraVars
        ) {
          var event =
            el.tagName.toLowerCase() === 'select' ||
            ['checkbox', 'radio'].includes(el.type) ||
            modifiers.includes('lazy')
              ? 'change'
              : 'input';
          let listenerExpression = `${expression} = rightSideOfExpression($event, ${expression})`;
          registerListener(component, el, event, modifiers, listenerExpression, () =>
            _objectSpread2(
              _objectSpread2({}, extraVars()),
              {},
              {
                rightSideOfExpression: generateModelAssignmentFunction(
                  el,
                  modifiers,
                  expression
                ),
              }
            )
          );
        }
        function generateModelAssignmentFunction(el, modifiers, expression) {
          return (
            el.type === 'radio' &&
              (el.hasAttribute('name') || el.setAttribute('name', expression)),
            (event, currentValue) => {
              if (event instanceof CustomEvent && event.detail) return event.detail;
              if (el.type === 'checkbox')
                if (Array.isArray(currentValue)) {
                  let newValue = modifiers.includes('number')
                    ? safeParseNumber(event.target.value)
                    : event.target.value;
                  return event.target.checked
                    ? currentValue.concat([newValue])
                    : currentValue.filter(
                        (el2) => !checkedAttrLooseCompare(el2, newValue)
                      );
                } else return event.target.checked;
              else {
                if (el.tagName.toLowerCase() === 'select' && el.multiple)
                  return modifiers.includes('number')
                    ? Array.from(event.target.selectedOptions).map((option2) => {
                        let rawValue = option2.value || option2.text;
                        return safeParseNumber(rawValue);
                      })
                    : Array.from(event.target.selectedOptions).map(
                        (option2) => option2.value || option2.text
                      );
                {
                  let rawValue = event.target.value;
                  return modifiers.includes('number')
                    ? safeParseNumber(rawValue)
                    : modifiers.includes('trim')
                    ? rawValue.trim()
                    : rawValue;
                }
              }
            }
          );
        }
        function safeParseNumber(rawValue) {
          let number = rawValue ? parseFloat(rawValue) : null;
          return isNumeric(number) ? number : rawValue;
        }
        let { isArray } = Array,
          {
            getPrototypeOf,
            create: ObjectCreate,
            defineProperty: ObjectDefineProperty,
            defineProperties: ObjectDefineProperties,
            isExtensible,
            getOwnPropertyDescriptor,
            getOwnPropertyNames,
            getOwnPropertySymbols,
            preventExtensions,
            hasOwnProperty,
          } = Object,
          { push: ArrayPush, concat: ArrayConcat, map: ArrayMap } = Array.prototype;
        function isUndefined(obj) {
          return obj === void 0;
        }
        function isFunction(obj) {
          return typeof obj == 'function';
        }
        function isObject(obj) {
          return typeof obj == 'object';
        }
        let proxyToValueMap = new WeakMap();
        function registerProxy(proxy, value) {
          proxyToValueMap.set(proxy, value);
        }
        let unwrap = (replicaOrAny) =>
          proxyToValueMap.get(replicaOrAny) || replicaOrAny;
        function wrapValue(membrane, value) {
          return membrane.valueIsObservable(value) ? membrane.getProxy(value) : value;
        }
        function unwrapDescriptor(descriptor) {
          return (
            hasOwnProperty.call(descriptor, 'value') &&
              (descriptor.value = unwrap(descriptor.value)),
            descriptor
          );
        }
        function lockShadowTarget(membrane, shadowTarget, originalTarget) {
          ArrayConcat.call(
            getOwnPropertyNames(originalTarget),
            getOwnPropertySymbols(originalTarget)
          ).forEach((key) => {
            let descriptor = getOwnPropertyDescriptor(originalTarget, key);
            descriptor.configurable ||
              (descriptor = wrapDescriptor(membrane, descriptor, wrapValue)),
              ObjectDefineProperty(shadowTarget, key, descriptor);
          }),
            preventExtensions(shadowTarget);
        }
        class ReactiveProxyHandler {
          constructor(membrane, value) {
            (this.originalTarget = value), (this.membrane = membrane);
          }
          get(shadowTarget, key) {
            let { originalTarget, membrane } = this,
              value = originalTarget[key],
              { valueObserved } = membrane;
            return valueObserved(originalTarget, key), membrane.getProxy(value);
          }
          set(shadowTarget, key, value) {
            let {
              originalTarget,
              membrane: { valueMutated },
            } = this;
            return (
              originalTarget[key] !== value
                ? ((originalTarget[key] = value), valueMutated(originalTarget, key))
                : key === 'length' &&
                  isArray(originalTarget) &&
                  valueMutated(originalTarget, key),
              !0
            );
          }
          deleteProperty(shadowTarget, key) {
            let {
              originalTarget,
              membrane: { valueMutated },
            } = this;
            return delete originalTarget[key], valueMutated(originalTarget, key), !0;
          }
          apply(shadowTarget, thisArg, argArray) {}
          construct(target, argArray, newTarget) {}
          has(shadowTarget, key) {
            let {
              originalTarget,
              membrane: { valueObserved },
            } = this;
            return valueObserved(originalTarget, key), key in originalTarget;
          }
          ownKeys(shadowTarget) {
            let { originalTarget } = this;
            return ArrayConcat.call(
              getOwnPropertyNames(originalTarget),
              getOwnPropertySymbols(originalTarget)
            );
          }
          isExtensible(shadowTarget) {
            let shadowIsExtensible = isExtensible(shadowTarget);
            if (!shadowIsExtensible) return shadowIsExtensible;
            let { originalTarget, membrane } = this,
              targetIsExtensible = isExtensible(originalTarget);
            return (
              targetIsExtensible ||
                lockShadowTarget(membrane, shadowTarget, originalTarget),
              targetIsExtensible
            );
          }
          setPrototypeOf(shadowTarget, prototype) {}
          getPrototypeOf(shadowTarget) {
            let { originalTarget } = this;
            return getPrototypeOf(originalTarget);
          }
          getOwnPropertyDescriptor(shadowTarget, key) {
            let { originalTarget, membrane } = this,
              { valueObserved } = this.membrane;
            valueObserved(originalTarget, key);
            let desc = getOwnPropertyDescriptor(originalTarget, key);
            if (isUndefined(desc)) return desc;
            let shadowDescriptor = getOwnPropertyDescriptor(shadowTarget, key);
            return isUndefined(shadowDescriptor)
              ? ((desc = wrapDescriptor(membrane, desc, wrapValue)),
                desc.configurable || ObjectDefineProperty(shadowTarget, key, desc),
                desc)
              : shadowDescriptor;
          }
          preventExtensions(shadowTarget) {
            let { originalTarget, membrane } = this;
            return (
              lockShadowTarget(membrane, shadowTarget, originalTarget),
              preventExtensions(originalTarget),
              !0
            );
          }
          defineProperty(shadowTarget, key, descriptor) {
            let { originalTarget, membrane } = this,
              { valueMutated } = membrane,
              { configurable } = descriptor;
            if (
              hasOwnProperty.call(descriptor, 'writable') &&
              !hasOwnProperty.call(descriptor, 'value')
            ) {
              let originalDescriptor = getOwnPropertyDescriptor(originalTarget, key);
              descriptor.value = originalDescriptor.value;
            }
            return (
              ObjectDefineProperty(originalTarget, key, unwrapDescriptor(descriptor)),
              configurable === !1 &&
                ObjectDefineProperty(
                  shadowTarget,
                  key,
                  wrapDescriptor(membrane, descriptor, wrapValue)
                ),
              valueMutated(originalTarget, key),
              !0
            );
          }
        }
        function wrapReadOnlyValue(membrane, value) {
          return membrane.valueIsObservable(value)
            ? membrane.getReadOnlyProxy(value)
            : value;
        }
        class ReadOnlyHandler {
          constructor(membrane, value) {
            (this.originalTarget = value), (this.membrane = membrane);
          }
          get(shadowTarget, key) {
            let { membrane, originalTarget } = this,
              value = originalTarget[key],
              { valueObserved } = membrane;
            return valueObserved(originalTarget, key), membrane.getReadOnlyProxy(value);
          }
          set(shadowTarget, key, value) {
            return !1;
          }
          deleteProperty(shadowTarget, key) {
            return !1;
          }
          apply(shadowTarget, thisArg, argArray) {}
          construct(target, argArray, newTarget) {}
          has(shadowTarget, key) {
            let {
              originalTarget,
              membrane: { valueObserved },
            } = this;
            return valueObserved(originalTarget, key), key in originalTarget;
          }
          ownKeys(shadowTarget) {
            let { originalTarget } = this;
            return ArrayConcat.call(
              getOwnPropertyNames(originalTarget),
              getOwnPropertySymbols(originalTarget)
            );
          }
          setPrototypeOf(shadowTarget, prototype) {}
          getOwnPropertyDescriptor(shadowTarget, key) {
            let { originalTarget, membrane } = this,
              { valueObserved } = membrane;
            valueObserved(originalTarget, key);
            let desc = getOwnPropertyDescriptor(originalTarget, key);
            if (isUndefined(desc)) return desc;
            let shadowDescriptor = getOwnPropertyDescriptor(shadowTarget, key);
            return isUndefined(shadowDescriptor)
              ? ((desc = wrapDescriptor(membrane, desc, wrapReadOnlyValue)),
                hasOwnProperty.call(desc, 'set') && (desc.set = void 0),
                desc.configurable || ObjectDefineProperty(shadowTarget, key, desc),
                desc)
              : shadowDescriptor;
          }
          preventExtensions(shadowTarget) {
            return !1;
          }
          defineProperty(shadowTarget, key, descriptor) {
            return !1;
          }
        }
        function createShadowTarget(value) {
          let shadowTarget;
          return (
            isArray(value)
              ? (shadowTarget = [])
              : isObject(value) && (shadowTarget = {}),
            shadowTarget
          );
        }
        let ObjectDotPrototype = Object.prototype;
        function defaultValueIsObservable(value) {
          if (value === null || typeof value != 'object') return !1;
          if (isArray(value)) return !0;
          let proto = getPrototypeOf(value);
          return (
            proto === ObjectDotPrototype ||
            proto === null ||
            getPrototypeOf(proto) === null
          );
        }
        let defaultValueObserved = (obj, key) => {},
          defaultValueMutated = (obj, key) => {},
          defaultValueDistortion = (value) => value;
        function wrapDescriptor(membrane, descriptor, getValue) {
          let { set, get } = descriptor;
          return (
            hasOwnProperty.call(descriptor, 'value')
              ? (descriptor.value = getValue(membrane, descriptor.value))
              : (isUndefined(get) ||
                  (descriptor.get = function () {
                    return getValue(membrane, get.call(unwrap(this)));
                  }),
                isUndefined(set) ||
                  (descriptor.set = function (value) {
                    set.call(unwrap(this), membrane.unwrapProxy(value));
                  })),
            descriptor
          );
        }
        class ReactiveMembrane {
          constructor(options) {
            if (
              ((this.valueDistortion = defaultValueDistortion),
              (this.valueMutated = defaultValueMutated),
              (this.valueObserved = defaultValueObserved),
              (this.valueIsObservable = defaultValueIsObservable),
              (this.objectGraph = new WeakMap()),
              !isUndefined(options))
            ) {
              let {
                valueDistortion,
                valueMutated,
                valueObserved,
                valueIsObservable,
              } = options;
              (this.valueDistortion = isFunction(valueDistortion)
                ? valueDistortion
                : defaultValueDistortion),
                (this.valueMutated = isFunction(valueMutated)
                  ? valueMutated
                  : defaultValueMutated),
                (this.valueObserved = isFunction(valueObserved)
                  ? valueObserved
                  : defaultValueObserved),
                (this.valueIsObservable = isFunction(valueIsObservable)
                  ? valueIsObservable
                  : defaultValueIsObservable);
            }
          }
          getProxy(value) {
            let unwrappedValue = unwrap(value),
              distorted = this.valueDistortion(unwrappedValue);
            if (this.valueIsObservable(distorted)) {
              let o = this.getReactiveState(unwrappedValue, distorted);
              return o.readOnly === value ? value : o.reactive;
            }
            return distorted;
          }
          getReadOnlyProxy(value) {
            value = unwrap(value);
            let distorted = this.valueDistortion(value);
            return this.valueIsObservable(distorted)
              ? this.getReactiveState(value, distorted).readOnly
              : distorted;
          }
          unwrapProxy(p) {
            return unwrap(p);
          }
          getReactiveState(value, distortedValue) {
            let { objectGraph } = this,
              reactiveState = objectGraph.get(distortedValue);
            if (reactiveState) return reactiveState;
            let membrane = this;
            return (
              (reactiveState = {
                get reactive() {
                  let reactiveHandler = new ReactiveProxyHandler(
                      membrane,
                      distortedValue
                    ),
                    proxy = new Proxy(
                      createShadowTarget(distortedValue),
                      reactiveHandler
                    );
                  return (
                    registerProxy(proxy, value),
                    ObjectDefineProperty(this, 'reactive', { value: proxy }),
                    proxy
                  );
                },
                get readOnly() {
                  let readOnlyHandler = new ReadOnlyHandler(membrane, distortedValue),
                    proxy = new Proxy(
                      createShadowTarget(distortedValue),
                      readOnlyHandler
                    );
                  return (
                    registerProxy(proxy, value),
                    ObjectDefineProperty(this, 'readOnly', { value: proxy }),
                    proxy
                  );
                },
              }),
              objectGraph.set(distortedValue, reactiveState),
              reactiveState
            );
          }
        }
        function wrap(data, mutationCallback) {
          let membrane = new ReactiveMembrane({
            valueMutated(target, key) {
              mutationCallback(target, key);
            },
          });
          return { data: membrane.getProxy(data), membrane };
        }
        function unwrap$1(membrane, observable) {
          let unwrappedData = membrane.unwrapProxy(observable),
            copy = {};
          return (
            Object.keys(unwrappedData).forEach((key) => {
              ['$el', '$refs', '$nextTick', '$watch'].includes(key) ||
                (copy[key] = unwrappedData[key]);
            }),
            copy
          );
        }
        class Component {
          constructor(el, componentForClone = null) {
            this.$el = el;
            let dataAttr = this.$el.getAttribute('x-data'),
              dataExpression = dataAttr === '' ? '{}' : dataAttr,
              initExpression = this.$el.getAttribute('x-init'),
              dataExtras = { $el: this.$el },
              canonicalComponentElementReference = componentForClone
                ? componentForClone.$el
                : this.$el;
            Object.entries(Alpine.magicProperties).forEach(([name, callback]) => {
              Object.defineProperty(dataExtras, `$${name}`, {
                get: function () {
                  return callback(canonicalComponentElementReference);
                },
              });
            }),
              (this.unobservedData = componentForClone
                ? componentForClone.getUnobservedData()
                : saferEval(el, dataExpression, dataExtras));
            let { membrane, data } = this.wrapDataInObservable(this.unobservedData);
            (this.$data = data),
              (this.membrane = membrane),
              (this.unobservedData.$el = this.$el),
              (this.unobservedData.$refs = this.getRefsProxy()),
              (this.nextTickStack = []),
              (this.unobservedData.$nextTick = (callback) => {
                this.nextTickStack.push(callback);
              }),
              (this.watchers = {}),
              (this.unobservedData.$watch = (property, callback) => {
                this.watchers[property] || (this.watchers[property] = []),
                  this.watchers[property].push(callback);
              }),
              Object.entries(Alpine.magicProperties).forEach(([name, callback]) => {
                Object.defineProperty(this.unobservedData, `$${name}`, {
                  get: function () {
                    return callback(canonicalComponentElementReference, this.$el);
                  },
                });
              }),
              (this.showDirectiveStack = []),
              this.showDirectiveLastElement,
              componentForClone ||
                Alpine.onBeforeComponentInitializeds.forEach((callback) =>
                  callback(this)
                );
            var initReturnedCallback;
            initExpression &&
              !componentForClone &&
              ((this.pauseReactivity = !0),
              (initReturnedCallback = this.evaluateReturnExpression(
                this.$el,
                initExpression
              )),
              (this.pauseReactivity = !1)),
              this.initializeElements(this.$el, () => {}, componentForClone),
              this.listenForNewElementsToInitialize(),
              typeof initReturnedCallback == 'function' &&
                initReturnedCallback.call(this.$data),
              componentForClone ||
                setTimeout(() => {
                  Alpine.onComponentInitializeds.forEach((callback) => callback(this));
                }, 0);
          }
          getUnobservedData() {
            return unwrap$1(this.membrane, this.$data);
          }
          wrapDataInObservable(data) {
            var self2 = this;
            let updateDom = debounce(function () {
              self2.updateElements(self2.$el);
            }, 0);
            return wrap(data, (target, key) => {
              self2.watchers[key]
                ? self2.watchers[key].forEach((callback) => callback(target[key]))
                : Array.isArray(target)
                ? Object.keys(self2.watchers).forEach((fullDotNotationKey) => {
                    let dotNotationParts = fullDotNotationKey.split('.');
                    key !== 'length' &&
                      dotNotationParts.reduce(
                        (comparisonData, part) => (
                          Object.is(target, comparisonData[part]) &&
                            self2.watchers[fullDotNotationKey].forEach((callback) =>
                              callback(target)
                            ),
                          comparisonData[part]
                        ),
                        self2.unobservedData
                      );
                  })
                : Object.keys(self2.watchers)
                    .filter((i) => i.includes('.'))
                    .forEach((fullDotNotationKey) => {
                      let dotNotationParts = fullDotNotationKey.split('.');
                      key === dotNotationParts[dotNotationParts.length - 1] &&
                        dotNotationParts.reduce(
                          (comparisonData, part) => (
                            Object.is(target, comparisonData) &&
                              self2.watchers[fullDotNotationKey].forEach((callback) =>
                                callback(target[key])
                              ),
                            comparisonData[part]
                          ),
                          self2.unobservedData
                        );
                    }),
                !self2.pauseReactivity && updateDom();
            });
          }
          walkAndSkipNestedComponents(
            el,
            callback,
            initializeComponentCallback = () => {}
          ) {
            walk(el, (el2) =>
              el2.hasAttribute('x-data') && !el2.isSameNode(this.$el)
                ? (el2.__x || initializeComponentCallback(el2), !1)
                : callback(el2)
            );
          }
          initializeElements(rootEl2, extraVars = () => {}, componentForClone = !1) {
            this.walkAndSkipNestedComponents(
              rootEl2,
              (el) => {
                if (el.__x_for_key !== void 0 || el.__x_inserted_me !== void 0)
                  return !1;
                this.initializeElement(el, extraVars, !componentForClone);
              },
              (el) => {
                componentForClone || (el.__x = new Component(el));
              }
            ),
              this.executeAndClearRemainingShowDirectiveStack(),
              this.executeAndClearNextTickStack(rootEl2);
          }
          initializeElement(el, extraVars, shouldRegisterListeners = !0) {
            el.hasAttribute('class') &&
              getXAttrs(el, this).length > 0 &&
              (el.__x_original_classes = convertClassStringToArray(
                el.getAttribute('class')
              )),
              shouldRegisterListeners && this.registerListeners(el, extraVars),
              this.resolveBoundAttributes(el, !0, extraVars);
          }
          updateElements(rootEl2, extraVars = () => {}) {
            this.walkAndSkipNestedComponents(
              rootEl2,
              (el) => {
                if (el.__x_for_key !== void 0 && !el.isSameNode(this.$el)) return !1;
                this.updateElement(el, extraVars);
              },
              (el) => {
                el.__x = new Component(el);
              }
            ),
              this.executeAndClearRemainingShowDirectiveStack(),
              this.executeAndClearNextTickStack(rootEl2);
          }
          executeAndClearNextTickStack(el) {
            el === this.$el &&
              this.nextTickStack.length > 0 &&
              requestAnimationFrame(() => {
                for (; this.nextTickStack.length > 0; ) this.nextTickStack.shift()();
              });
          }
          executeAndClearRemainingShowDirectiveStack() {
            this.showDirectiveStack
              .reverse()
              .map(
                (handler) =>
                  new Promise((resolve, reject) => {
                    handler(resolve, reject);
                  })
              )
              .reduce(
                (promiseChain, promise) =>
                  promiseChain.then(() =>
                    promise.then((finishElement) => {
                      finishElement();
                    })
                  ),
                Promise.resolve(() => {})
              )
              .catch((e) => {
                if (e !== TRANSITION_CANCELLED) throw e;
              }),
              (this.showDirectiveStack = []),
              (this.showDirectiveLastElement = void 0);
          }
          updateElement(el, extraVars) {
            this.resolveBoundAttributes(el, !1, extraVars);
          }
          registerListeners(el, extraVars) {
            getXAttrs(el, this).forEach(({ type, value, modifiers, expression }) => {
              switch (type) {
                case 'on':
                  registerListener(this, el, value, modifiers, expression, extraVars);
                  break;
                case 'model':
                  registerModelListener(this, el, modifiers, expression, extraVars);
                  break;
              }
            });
          }
          resolveBoundAttributes(el, initialUpdate = !1, extraVars) {
            let attrs = getXAttrs(el, this);
            attrs.forEach(({ type, value, modifiers, expression }) => {
              switch (type) {
                case 'model':
                  handleAttributeBindingDirective(
                    this,
                    el,
                    'value',
                    expression,
                    extraVars,
                    type,
                    modifiers
                  );
                  break;
                case 'bind':
                  if (el.tagName.toLowerCase() === 'template' && value === 'key')
                    return;
                  handleAttributeBindingDirective(
                    this,
                    el,
                    value,
                    expression,
                    extraVars,
                    type,
                    modifiers
                  );
                  break;
                case 'text':
                  var output = this.evaluateReturnExpression(el, expression, extraVars);
                  handleTextDirective(el, output, expression);
                  break;
                case 'html':
                  handleHtmlDirective(this, el, expression, extraVars);
                  break;
                case 'show':
                  var output = this.evaluateReturnExpression(el, expression, extraVars);
                  handleShowDirective(this, el, output, modifiers, initialUpdate);
                  break;
                case 'if':
                  if (attrs.some((i) => i.type === 'for')) return;
                  var output = this.evaluateReturnExpression(el, expression, extraVars);
                  handleIfDirective(this, el, output, initialUpdate, extraVars);
                  break;
                case 'for':
                  handleForDirective(this, el, expression, initialUpdate, extraVars);
                  break;
                case 'cloak':
                  el.removeAttribute('x-cloak');
                  break;
              }
            });
          }
          evaluateReturnExpression(el, expression, extraVars = () => {}) {
            return saferEval(
              el,
              expression,
              this.$data,
              _objectSpread2(
                _objectSpread2({}, extraVars()),
                {},
                { $dispatch: this.getDispatchFunction(el) }
              )
            );
          }
          evaluateCommandExpression(el, expression, extraVars = () => {}) {
            return saferEvalNoReturn(
              el,
              expression,
              this.$data,
              _objectSpread2(
                _objectSpread2({}, extraVars()),
                {},
                { $dispatch: this.getDispatchFunction(el) }
              )
            );
          }
          getDispatchFunction(el) {
            return (event, detail = {}) => {
              el.dispatchEvent(new CustomEvent(event, { detail, bubbles: !0 }));
            };
          }
          listenForNewElementsToInitialize() {
            let targetNode = this.$el,
              observerOptions = { childList: !0, attributes: !0, subtree: !0 };
            new MutationObserver((mutations) => {
              for (let i = 0; i < mutations.length; i++) {
                let closestParentComponent = mutations[i].target.closest('[x-data]');
                if (
                  !!(
                    closestParentComponent &&
                    closestParentComponent.isSameNode(this.$el)
                  )
                ) {
                  if (
                    mutations[i].type === 'attributes' &&
                    mutations[i].attributeName === 'x-data'
                  ) {
                    let xAttr = mutations[i].target.getAttribute('x-data') || '{}',
                      rawData = saferEval(this.$el, xAttr, { $el: this.$el });
                    Object.keys(rawData).forEach((key) => {
                      this.$data[key] !== rawData[key] &&
                        (this.$data[key] = rawData[key]);
                    });
                  }
                  mutations[i].addedNodes.length > 0 &&
                    mutations[i].addedNodes.forEach((node) => {
                      if (!(node.nodeType !== 1 || node.__x_inserted_me)) {
                        if (node.matches('[x-data]') && !node.__x) {
                          node.__x = new Component(node);
                          return;
                        }
                        this.initializeElements(node);
                      }
                    });
                }
              }
            }).observe(targetNode, observerOptions);
          }
          getRefsProxy() {
            var self2 = this,
              refObj = {};
            return new Proxy(refObj, {
              get(object, property) {
                if (property === '$isAlpineProxy') return !0;
                var ref;
                return (
                  self2.walkAndSkipNestedComponents(self2.$el, (el) => {
                    el.hasAttribute('x-ref') &&
                      el.getAttribute('x-ref') === property &&
                      (ref = el);
                  }),
                  ref
                );
              },
            });
          }
        }
        let Alpine = {
          version: '2.8.2',
          pauseMutationObserver: !1,
          magicProperties: {},
          onComponentInitializeds: [],
          onBeforeComponentInitializeds: [],
          ignoreFocusedForValueBinding: !1,
          start: async function () {
            isTesting() || (await domReady()),
              this.discoverComponents((el) => {
                this.initializeComponent(el);
              }),
              document.addEventListener('turbolinks:load', () => {
                this.discoverUninitializedComponents((el) => {
                  this.initializeComponent(el);
                });
              }),
              this.listenForNewUninitializedComponentsAtRunTime();
          },
          discoverComponents: function (callback) {
            document.querySelectorAll('[x-data]').forEach((rootEl2) => {
              callback(rootEl2);
            });
          },
          discoverUninitializedComponents: function (callback, el = null) {
            let rootEls = (el || document).querySelectorAll('[x-data]');
            Array.from(rootEls)
              .filter((el2) => el2.__x === void 0)
              .forEach((rootEl2) => {
                callback(rootEl2);
              });
          },
          listenForNewUninitializedComponentsAtRunTime: function () {
            let targetNode = document.querySelector('body'),
              observerOptions = { childList: !0, attributes: !0, subtree: !0 };
            new MutationObserver((mutations) => {
              if (!this.pauseMutationObserver)
                for (let i = 0; i < mutations.length; i++)
                  mutations[i].addedNodes.length > 0 &&
                    mutations[i].addedNodes.forEach((node) => {
                      node.nodeType === 1 &&
                        ((node.parentElement &&
                          node.parentElement.closest('[x-data]')) ||
                          this.discoverUninitializedComponents((el) => {
                            this.initializeComponent(el);
                          }, node.parentElement));
                    });
            }).observe(targetNode, observerOptions);
          },
          initializeComponent: function (el) {
            if (!el.__x)
              try {
                el.__x = new Component(el);
              } catch (error) {
                setTimeout(() => {
                  throw error;
                }, 0);
              }
          },
          clone: function (component, newEl) {
            newEl.__x || (newEl.__x = new Component(newEl, component));
          },
          addMagicProperty: function (name, callback) {
            this.magicProperties[name] = callback;
          },
          onComponentInitialized: function (callback) {
            this.onComponentInitializeds.push(callback);
          },
          onBeforeComponentInitialized: function (callback) {
            this.onBeforeComponentInitializeds.push(callback);
          },
        };
        return (
          isTesting() ||
            ((window.Alpine = Alpine),
            window.deferLoadingAlpine
              ? window.deferLoadingAlpine(function () {
                  window.Alpine.start();
                })
              : window.Alpine.start()),
          Alpine
        );
      });
    },
  });
  var require_htmx_min = __commonJS({
    'node_modules/htmx.org/dist/htmx.min.js'(exports, module) {
      (function (e, t) {
        typeof define == 'function' && define.amd ? define([], t) : (e.htmx = t());
      })(typeof self != 'undefined' ? self : exports, function () {
        return (function () {
          'use strict';
          var v = {
              onLoad: b,
              process: rt,
              on: z,
              off: V,
              trigger: lt,
              ajax: $t,
              find: S,
              findAll: E,
              closest: T,
              values: function (e, t) {
                var r = Rt(e, t || 'post');
                return r.values;
              },
              remove: C,
              addClass: O,
              removeClass: A,
              toggleClass: L,
              takeClass: R,
              defineExtension: Kt,
              removeExtension: Qt,
              logAll: w,
              logger: null,
              config: {
                historyEnabled: !0,
                historyCacheSize: 10,
                refreshOnHistoryMiss: !1,
                defaultSwapStyle: 'innerHTML',
                defaultSwapDelay: 0,
                defaultSettleDelay: 100,
                includeIndicatorStyles: !0,
                indicatorClass: 'htmx-indicator',
                requestClass: 'htmx-request',
                settlingClass: 'htmx-settling',
                swappingClass: 'htmx-swapping',
                allowEval: !0,
                attributesToSettle: ['class', 'style', 'width', 'height'],
                wsReconnectDelay: 'full-jitter',
                disableSelector: '[hx-disable], [data-hx-disable]',
              },
              parseInterval: f,
              _: e,
              createEventSource: function (e) {
                return new EventSource(e, { withCredentials: !0 });
              },
              createWebSocket: function (e) {
                return new WebSocket(e, []);
              },
            },
            t = ['get', 'post', 'put', 'delete', 'patch'],
            n = t
              .map(function (e) {
                return '[hx-' + e + '], [data-hx-' + e + ']';
              })
              .join(', ');
          function f(e) {
            if (e != null)
              return e.slice(-2) == 'ms'
                ? parseFloat(e.slice(0, -2)) || void 0
                : e.slice(-1) == 's'
                ? parseFloat(e.slice(0, -1)) * 1e3 || void 0
                : parseFloat(e) || void 0;
          }
          function l(e, t) {
            return e.getAttribute && e.getAttribute(t);
          }
          function a(e, t) {
            return e.hasAttribute && (e.hasAttribute(t) || e.hasAttribute('data-' + t));
          }
          function I(e, t) {
            return l(e, t) || l(e, 'data-' + t);
          }
          function c(e) {
            return e.parentElement;
          }
          function M() {
            return document;
          }
          function h(e, t) {
            return t(e) ? e : c(e) ? h(c(e), t) : null;
          }
          function k(e, t) {
            var r = null;
            return (
              h(e, function (e2) {
                return (r = I(e2, t));
              }),
              r
            );
          }
          function d(e, t) {
            var r =
              e.matches ||
              e.matchesSelector ||
              e.msMatchesSelector ||
              e.mozMatchesSelector ||
              e.webkitMatchesSelector ||
              e.oMatchesSelector;
            return r && r.call(e, t);
          }
          function r(e) {
            var t = /<([a-z][^\/\0>\x20\t\r\n\f]*)/i,
              r = t.exec(e);
            return r ? r[1].toLowerCase() : '';
          }
          function i(e, t) {
            for (
              var r = new DOMParser(),
                n = r.parseFromString(e, 'text/html'),
                i = n.body;
              t > 0;

            )
              t--, (i = i.firstChild);
            return i == null && (i = M().createDocumentFragment()), i;
          }
          function u(e) {
            var t = r(e);
            switch (t) {
              case 'thead':
              case 'tbody':
              case 'tfoot':
              case 'colgroup':
              case 'caption':
                return i('<table>' + e + '</table>', 1);
              case 'col':
                return i('<table><colgroup>' + e + '</colgroup></table>', 2);
              case 'tr':
                return i('<table><tbody>' + e + '</tbody></table>', 2);
              case 'td':
              case 'th':
                return i('<table><tbody><tr>' + e + '</tr></tbody></table>', 3);
              case 'script':
                return i('<div>' + e + '</div>', 1);
              default:
                return i(e, 0);
            }
          }
          function D(e) {
            e && e();
          }
          function o(e, t) {
            return Object.prototype.toString.call(e) === '[object ' + t + ']';
          }
          function s(e) {
            return o(e, 'Function');
          }
          function g(e) {
            return o(e, 'Object');
          }
          function F(e) {
            var t = 'htmx-internal-data',
              r = e[t];
            return r || (r = e[t] = {}), r;
          }
          function p(e) {
            var t = [];
            if (e) for (var r = 0; r < e.length; r++) t.push(e[r]);
            return t;
          }
          function X(e, t) {
            if (e) for (var r = 0; r < e.length; r++) t(e[r]);
          }
          function m(e) {
            var t = e.getBoundingClientRect(),
              r = t.top,
              n = t.bottom;
            return r < window.innerHeight && n >= 0;
          }
          function P(e) {
            return M().body.contains(e);
          }
          function y(e) {
            return e.trim().split(/\s+/);
          }
          function U(e, t) {
            for (var r in t) t.hasOwnProperty(r) && (e[r] = t[r]);
            return e;
          }
          function x(e) {
            try {
              return JSON.parse(e);
            } catch (e2) {
              return ut(e2), null;
            }
          }
          function e(e) {
            return Ut(M().body, function () {
              return eval(e);
            });
          }
          function b(t) {
            var e = v.on('htmx:load', function (e2) {
              t(e2.detail.elt);
            });
            return e;
          }
          function w() {
            v.logger = function (e, t, r) {
              console && console.log(t, e, r);
            };
          }
          function S(e, t) {
            return t ? e.querySelector(t) : S(M(), e);
          }
          function E(e, t) {
            return t ? e.querySelectorAll(t) : E(M(), e);
          }
          function C(e, t) {
            (e = N(e)),
              t
                ? setTimeout(function () {
                    C(e);
                  }, t)
                : e.parentElement.removeChild(e);
          }
          function O(e, t, r) {
            (e = N(e)),
              r
                ? setTimeout(function () {
                    O(e, t);
                  }, r)
                : e.classList.add(t);
          }
          function A(e, t, r) {
            (e = N(e)),
              r
                ? setTimeout(function () {
                    A(e, t);
                  }, r)
                : e.classList.remove(t);
          }
          function L(e, t) {
            (e = N(e)), e.classList.toggle(t);
          }
          function R(e, t) {
            (e = N(e)),
              X(e.parentElement.children, function (e2) {
                A(e2, t);
              }),
              O(e, t);
          }
          function T(e, t) {
            if (((e = N(e)), e.closest)) return e.closest(t);
            do if (e == null || d(e, t)) return e;
            while ((e = e && c(e)));
          }
          function q(e, t) {
            return t.indexOf('closest ') === 0
              ? [T(e, t.substr(8))]
              : t.indexOf('find ') === 0
              ? [S(e, t.substr(5))]
              : M().querySelectorAll(t);
          }
          function H(e, t) {
            return q(e, t)[0];
          }
          function N(e) {
            return o(e, 'String') ? S(e) : e;
          }
          function j(e, t, r) {
            return s(t)
              ? { target: M().body, event: e, listener: t }
              : { target: N(e), event: t, listener: r };
          }
          function z(t, r, n) {
            tr(function () {
              var e2 = j(t, r, n);
              e2.target.addEventListener(e2.event, e2.listener);
            });
            var e = s(r);
            return e ? r : n;
          }
          function V(t, r, n) {
            return (
              tr(function () {
                var e = j(t, r, n);
                e.target.removeEventListener(e.event, e.listener);
              }),
              s(r) ? r : n
            );
          }
          function W(e) {
            var t = h(e, function (e2) {
              return I(e2, 'hx-target') !== null;
            });
            if (t) {
              var r = I(t, 'hx-target');
              return r === 'this' ? t : H(e, r);
            } else {
              var n = F(e);
              return n.boosted ? M().body : e;
            }
          }
          function _(e) {
            for (var t = v.config.attributesToSettle, r = 0; r < t.length; r++)
              if (e === t[r]) return !0;
            return !1;
          }
          function B(t, r) {
            X(t.attributes, function (e) {
              !r.hasAttribute(e.name) && _(e.name) && t.removeAttribute(e.name);
            }),
              X(r.attributes, function (e) {
                _(e.name) && t.setAttribute(e.name, e.value);
              });
          }
          function $(e, t) {
            for (var r = er(t), n = 0; n < r.length; n++) {
              var i = r[n];
              try {
                if (i.isInlineSwap(e)) return !0;
              } catch (e2) {
                ut(e2);
              }
            }
            return e === 'outerHTML';
          }
          function J(e, t, r) {
            var n = '#' + t.id,
              i = 'outerHTML';
            e === 'true' ||
              (e.indexOf(':') > 0
                ? ((i = e.substr(0, e.indexOf(':'))),
                  (n = e.substr(e.indexOf(':') + 1, e.length)))
                : (i = e));
            var o = M().querySelector(n);
            if (o) {
              var a;
              (a = M().createDocumentFragment()),
                a.appendChild(t),
                $(i, o) || (a = t),
                le(i, o, o, a, r);
            } else t.parentNode.removeChild(t), ot(M().body, 'htmx:oobErrorNoTarget', { content: t });
            return e;
          }
          function Z(e, r) {
            X(E(e, '[hx-swap-oob], [data-hx-swap-oob]'), function (e2) {
              var t = I(e2, 'hx-swap-oob');
              t != null && J(t, e2, r);
            });
          }
          function G(e) {
            X(E(e, '[hx-preserve], [data-hx-preserve]'), function (e2) {
              var t = I(e2, 'id'),
                r = M().getElementById(t);
              r != null && e2.parentNode.replaceChild(r, e2);
            });
          }
          function Y(n, e, i) {
            X(e.querySelectorAll('[id]'), function (e2) {
              if (e2.id && e2.id.length > 0) {
                var t = n.querySelector(e2.tagName + "[id='" + e2.id + "']");
                if (t && t !== n) {
                  var r = e2.cloneNode();
                  B(e2, t),
                    i.tasks.push(function () {
                      B(e2, r);
                    });
                }
              }
            });
          }
          function K(e) {
            return function () {
              rt(e), Ke(e), Q(e), lt(e, 'htmx:load');
            };
          }
          function Q(e) {
            var t = '[autofocus]',
              r = d(e, t) ? e : e.querySelector(t);
            r != null && r.focus();
          }
          function ee(e, t, r, n) {
            for (Y(e, r, n); r.childNodes.length > 0; ) {
              var i = r.firstChild;
              e.insertBefore(i, t),
                i.nodeType !== Node.TEXT_NODE &&
                  i.nodeType !== Node.COMMENT_NODE &&
                  n.tasks.push(K(i));
            }
          }
          function te(t) {
            var e = F(t);
            e.webSocket && e.webSocket.close(),
              e.sseEventSource && e.sseEventSource.close(),
              e.listenerInfos &&
                X(e.listenerInfos, function (e2) {
                  t !== e2.on && e2.on.removeEventListener(e2.trigger, e2.listener);
                }),
              t.children &&
                X(t.children, function (e2) {
                  te(e2);
                });
          }
          function re(e, t, r) {
            if (e.tagName === 'BODY') return se(e, t);
            var n = e.previousSibling;
            if ((ee(c(e), e, t, r), n == null)) var i = c(e).firstChild;
            else var i = n.nextSibling;
            for (F(e).replacedWith = i, r.elts = []; i && i !== e; )
              i.nodeType === Node.ELEMENT_NODE && r.elts.push(i),
                (i = i.nextElementSibling);
            te(e), c(e).removeChild(e);
          }
          function ne(e, t, r) {
            return ee(e, e.firstChild, t, r);
          }
          function ie(e, t, r) {
            return ee(c(e), e, t, r);
          }
          function oe(e, t, r) {
            return ee(e, null, t, r);
          }
          function ae(e, t, r) {
            return ee(c(e), e.nextSibling, t, r);
          }
          function se(e, t, r) {
            var n = e.firstChild;
            if ((ee(e, n, t, r), n)) {
              for (; n.nextSibling; ) te(n.nextSibling), e.removeChild(n.nextSibling);
              te(n), e.removeChild(n);
            }
          }
          function ue(e, t) {
            var r = k(e, 'hx-select');
            if (r) {
              var n = M().createDocumentFragment();
              X(t.querySelectorAll(r), function (e2) {
                n.appendChild(e2);
              }),
                (t = n);
            }
            return t;
          }
          function le(e, t, r, n, i) {
            switch (e) {
              case 'none':
                return;
              case 'outerHTML':
                re(r, n, i);
                return;
              case 'afterbegin':
                ne(r, n, i);
                return;
              case 'beforebegin':
                ie(r, n, i);
                return;
              case 'beforeend':
                oe(r, n, i);
                return;
              case 'afterend':
                ae(r, n, i);
                return;
              default:
                for (var o = er(t), a = 0; a < o.length; a++) {
                  var s = o[a];
                  try {
                    var u = s.handleSwap(e, r, n, i);
                    if (u) {
                      if (typeof u.length != 'undefined')
                        for (var l = 0; l < u.length; l++) {
                          var f = u[l];
                          f.nodeType !== Node.TEXT_NODE &&
                            f.nodeType !== Node.COMMENT_NODE &&
                            i.tasks.push(K(f));
                        }
                      return;
                    }
                  } catch (e2) {
                    ut(e2);
                  }
                }
                se(r, n, i);
            }
          }
          var fe = /<title>([\s\S]+?)<\/title>/im;
          function ce(e) {
            var t = fe.exec(e);
            if (t) return t[1];
          }
          function he(e, t, r, n, i) {
            var o = ce(n);
            if (o) {
              var a = S('title');
              a ? (a.innerHTML = o) : (window.document.title = o);
            }
            var s = u(n);
            if (s) return Z(s, i), (s = ue(r, s)), G(s), le(e, r, t, s, i);
          }
          function de(e, t, r) {
            var n = e.getResponseHeader(t);
            if (n.indexOf('{') === 0) {
              var i = x(n);
              for (var o in i)
                if (i.hasOwnProperty(o)) {
                  var a = i[o];
                  g(a) || (a = { value: a }), lt(r, o, a);
                }
            } else lt(r, n, []);
          }
          var ve = /\s/,
            ge = /[\s,]/,
            pe = /[_$a-zA-Z]/,
            me = /[_$a-zA-Z0-9]/,
            ye = ['"', "'", '/'],
            xe = /[^\s]/;
          function be(e) {
            for (var t = [], r = 0; r < e.length; ) {
              if (pe.exec(e.charAt(r))) {
                for (var n = r; me.exec(e.charAt(r + 1)); ) r++;
                t.push(e.substr(n, r - n + 1));
              } else if (ye.indexOf(e.charAt(r)) !== -1) {
                var i = e.charAt(r),
                  n = r;
                for (r++; r < e.length && e.charAt(r) !== i; )
                  e.charAt(r) === '\\' && r++, r++;
                t.push(e.substr(n, r - n + 1));
              } else {
                var o = e.charAt(r);
                t.push(o);
              }
              r++;
            }
            return t;
          }
          function we(e, t, r) {
            return (
              pe.exec(e.charAt(0)) &&
              e !== 'true' &&
              e !== 'false' &&
              e !== 'this' &&
              e !== r &&
              t !== '.'
            );
          }
          function Se(e, t, r) {
            if (t[0] === '[') {
              t.shift();
              for (
                var n = 1, i = ' return (function(' + r + '){ return (', o = null;
                t.length > 0;

              ) {
                var a = t[0];
                if (a === ']') {
                  if ((n--, n === 0)) {
                    o === null && (i = i + 'true'), t.shift(), (i += ')})');
                    try {
                      var s = Ut(
                        e,
                        function () {
                          return Function(i)();
                        },
                        function () {
                          return !0;
                        }
                      );
                      return (s.source = i), s;
                    } catch (e2) {
                      return (
                        ot(M().body, 'htmx:syntax:error', { error: e2, source: i }),
                        null
                      );
                    }
                  }
                } else a === '[' && n++;
                we(a, o, r)
                  ? (i +=
                      '((' +
                      r +
                      '.' +
                      a +
                      ') ? (' +
                      r +
                      '.' +
                      a +
                      ') : (window.' +
                      a +
                      '))')
                  : (i = i + a),
                  (o = t.shift());
              }
            }
          }
          function Ee(e, t) {
            for (var r = ''; e.length > 0 && !e[0].match(t); ) r += e.shift();
            return r;
          }
          var Ce = 'input, textarea, select';
          function Oe(e) {
            var t = I(e, 'hx-trigger'),
              r = [];
            if (t) {
              var n = be(t);
              do {
                Ee(n, xe);
                var i = n.length,
                  o = Ee(n, /[,\[\s]/);
                if (o !== '')
                  if (o === 'every') {
                    var a = { trigger: 'every' };
                    Ee(n, xe), (a.pollInterval = f(Ee(n, ve))), r.push(a);
                  } else if (o.indexOf('sse:') === 0)
                    r.push({ trigger: 'sse', sseEvent: o.substr(4) });
                  else {
                    var s = { trigger: o },
                      u = Se(e, n, 'event');
                    for (u && (s.eventFilter = u); n.length > 0 && n[0] !== ','; ) {
                      Ee(n, xe);
                      var l = n.shift();
                      l === 'changed'
                        ? (s.changed = !0)
                        : l === 'once'
                        ? (s.once = !0)
                        : l === 'consume'
                        ? (s.consume = !0)
                        : l === 'delay' && n[0] === ':'
                        ? (n.shift(), (s.delay = f(Ee(n, ge))))
                        : l === 'from' && n[0] === ':'
                        ? (n.shift(), (s.from = Ee(n, ge)))
                        : l === 'target' && n[0] === ':'
                        ? (n.shift(), (s.target = Ee(n, ge)))
                        : l === 'throttle' && n[0] === ':'
                        ? (n.shift(), (s.throttle = f(Ee(n, ge))))
                        : ot(e, 'htmx:syntax:error', { token: n.shift() });
                    }
                    r.push(s);
                  }
                n.length === i && ot(e, 'htmx:syntax:error', { token: n.shift() }),
                  Ee(n, xe);
              } while (n[0] === ',' && n.shift());
            }
            return r.length > 0
              ? r
              : d(e, 'form')
              ? [{ trigger: 'submit' }]
              : d(e, Ce)
              ? [{ trigger: 'change' }]
              : [{ trigger: 'click' }];
          }
          function Ae(e) {
            F(e).cancelled = !0;
          }
          function Le(e, t, r, n) {
            var i = F(e);
            i.timeout = setTimeout(function () {
              P(e) && i.cancelled !== !0 && (Jt(t, r, e), Le(e, t, I(e, 'hx-' + t), n));
            }, n);
          }
          function Re(e) {
            return (
              location.hostname === e.hostname &&
              l(e, 'href') &&
              l(e, 'href').indexOf('#') !== 0
            );
          }
          function Te(t, r, e) {
            if ((t.tagName === 'A' && Re(t)) || t.tagName === 'FORM') {
              r.boosted = !0;
              var n, i;
              if (t.tagName === 'A') (n = 'get'), (i = l(t, 'href'));
              else {
                var o = l(t, 'method');
                (n = o ? o.toLowerCase() : 'get'), (i = l(t, 'action'));
              }
              e.forEach(function (e2) {
                Ie(t, n, i, r, e2, !0);
              });
            }
          }
          function qe(e) {
            return (
              e.tagName === 'FORM' ||
              (d(e, 'input[type="submit"], button') && T(e, 'form') !== null) ||
              (e.tagName === 'A' &&
                e.href &&
                (e.getAttribute('href') === '#' ||
                  e.getAttribute('href').indexOf('#') !== 0))
            );
          }
          function He(e, t) {
            return F(e).boosted && e.tagName === 'A' && t.type === 'click' && t.ctrlKey;
          }
          function Ne(e, t) {
            var r = e.eventFilter;
            if (r)
              try {
                return r(t) !== !0;
              } catch (e2) {
                return (
                  ot(M().body, 'htmx:eventFilter:error', {
                    error: e2,
                    source: r.source,
                  }),
                  !0
                );
              }
            return !1;
          }
          function Ie(n, i, o, e, a, s) {
            var u = n;
            a.from && (u = S(a.from));
            var l = function (e2) {
              if (!P(n)) {
                u.removeEventListener(a.trigger, l);
                return;
              }
              if (!He(n, e2) && ((s || qe(n)) && e2.preventDefault(), !Ne(a, e2))) {
                var t = F(e2);
                t.handledFor == null && (t.handledFor = []);
                var r = F(n);
                if (t.handledFor.indexOf(n) < 0) {
                  if (
                    (t.handledFor.push(n),
                    a.consume && e2.stopPropagation(),
                    a.target && e2.target && !d(e2.target, a.target))
                  )
                    return;
                  if (a.once) {
                    if (r.triggeredOnce) return;
                    r.triggeredOnce = !0;
                  }
                  if (a.changed) {
                    if (r.lastValue === n.value) return;
                    r.lastValue = n.value;
                  }
                  if ((r.delayed && clearTimeout(r.delayed), r.throttle)) return;
                  a.throttle
                    ? (r.throttle = setTimeout(function () {
                        Jt(i, o, n, e2), (r.throttle = null);
                      }, a.throttle))
                    : a.delay
                    ? (r.delayed = setTimeout(function () {
                        Jt(i, o, n, e2);
                      }, a.delay))
                    : Jt(i, o, n, e2);
                }
              }
            };
            e.listenerInfos == null && (e.listenerInfos = []),
              e.listenerInfos.push({ trigger: a.trigger, listener: l, on: u }),
              u.addEventListener(a.trigger, l);
          }
          var Me = !1,
            ke = null;
          function De() {
            ke ||
              ((ke = function () {
                Me = !0;
              }),
              window.addEventListener('scroll', ke),
              setInterval(function () {
                Me &&
                  ((Me = !1),
                  X(
                    M().querySelectorAll(
                      "[hx-trigger='revealed'],[data-hx-trigger='revealed']"
                    ),
                    function (e) {
                      Fe(e);
                    }
                  ));
              }, 200));
          }
          function Fe(e) {
            var t = F(e);
            !t.revealed && m(e) && ((t.revealed = !0), Jt(t.verb, t.path, e));
          }
          function Xe(e, t, r) {
            for (var n = y(r), i = 0; i < n.length; i++) {
              var o = n[i].split(/:(.+)/);
              o[0] === 'connect' && Pe(e, o[1], 0), o[0] === 'send' && je(e);
            }
          }
          function Pe(s, r, n) {
            if (!!P(s)) {
              if (r.indexOf('/') == 0) {
                var e = location.hostname + (location.port ? ':' + location.port : '');
                location.protocol == 'https:'
                  ? (r = 'wss://' + e + r)
                  : location.protocol == 'http:' && (r = 'ws://' + e + r);
              }
              var t = v.createWebSocket(r);
              (t.onerror = function (e2) {
                ot(s, 'htmx:wsError', { error: e2, socket: t }), Ue(s);
              }),
                (t.onclose = function (e2) {
                  if ([1006, 1012, 1013].includes(e2.code)) {
                    var t2 = ze(n);
                    setTimeout(function () {
                      Pe(s, r, n + 1);
                    }, t2);
                  }
                }),
                (t.onopen = function (e2) {
                  n = 0;
                }),
                (F(s).webSocket = t),
                t.addEventListener('message', function (e2) {
                  if (!Ue(s)) {
                    var t2 = e2.data;
                    st(s, function (e3) {
                      t2 = e3.transformResponse(t2, null, s);
                    });
                    for (
                      var r2 = Ft(s), n2 = u(t2), i = p(n2.children), o = 0;
                      o < i.length;
                      o++
                    ) {
                      var a = i[o];
                      J(I(a, 'hx-swap-oob') || 'true', a, r2);
                    }
                    mt(r2.tasks);
                  }
                });
            }
          }
          function Ue(e) {
            if (!P(e)) return F(e).webSocket.close(), !0;
          }
          function je(l) {
            var f = h(l, function (e) {
              return F(e).webSocket != null;
            });
            f
              ? l.addEventListener(Oe(l)[0].trigger, function (e) {
                  var t = F(f).webSocket,
                    r = Nt(l, f),
                    n = Rt(l, 'post'),
                    i = n.errors,
                    o = n.values,
                    a = Vt(l),
                    s = U(o, a),
                    u = It(s, l);
                  if (((u.HEADERS = r), i && i.length > 0)) {
                    lt(l, 'htmx:validation:halted', i);
                    return;
                  }
                  t.send(JSON.stringify(u)), qe(l) && e.preventDefault();
                })
              : ot(l, 'htmx:noWebSocketSourceError');
          }
          function ze(e) {
            var t = v.config.wsReconnectDelay;
            if (typeof t == 'function') return t(e);
            if (t === 'full-jitter') {
              var r = Math.min(e, 6),
                n = 1e3 * Math.pow(2, r);
              return n * Math.random();
            }
            ut(
              'htmx.config.wsReconnectDelay must either be a function or the string "full-jitter"'
            );
          }
          function Ve(e, t, r) {
            for (var n = y(r), i = 0; i < n.length; i++) {
              var o = n[i].split(/:(.+)/);
              o[0] === 'connect' && We(e, o[1]), o[0] === 'swap' && _e(e, o[1]);
            }
          }
          function We(t, e) {
            var r = v.createEventSource(e);
            (r.onerror = function (e2) {
              ot(t, 'htmx:sseError', { error: e2, source: r }), $e(t);
            }),
              (F(t).sseEventSource = r);
          }
          function _e(o, a) {
            var s = h(o, Je);
            if (s) {
              var u = F(s).sseEventSource,
                l = function (e) {
                  if ($e(s)) {
                    u.removeEventListener(a, l);
                    return;
                  }
                  var t = e.data;
                  st(o, function (e2) {
                    t = e2.transformResponse(t, null, o);
                  });
                  var r = kt(o),
                    n = W(o),
                    i = Ft(o);
                  he(r.swapStyle, o, n, t, i), mt(i.tasks), lt(o, 'htmx:sseMessage', e);
                };
              (F(o).sseListener = l), u.addEventListener(a, l);
            } else ot(o, 'htmx:noSSESourceError');
          }
          function Be(e, t, r, n) {
            var i = h(e, Je);
            if (i) {
              var o = F(i).sseEventSource,
                a = function () {
                  $e(i) || (P(e) ? Jt(t, r, e) : o.removeEventListener(n, a));
                };
              (F(e).sseListener = a), o.addEventListener(n, a);
            } else ot(e, 'htmx:noSSESourceError');
          }
          function $e(e) {
            if (!P(e)) return F(e).sseEventSource.close(), !0;
          }
          function Je(e) {
            return F(e).sseEventSource != null;
          }
          function Ze(e, t, r, n, i) {
            var o = function () {
              n.loaded || ((n.loaded = !0), Jt(t, r, e));
            };
            i ? setTimeout(o, i) : o();
          }
          function Ge(n, i, e) {
            var o = !1;
            return (
              X(t, function (t) {
                if (a(n, 'hx-' + t)) {
                  var r = I(n, 'hx-' + t);
                  (o = !0),
                    (i.path = r),
                    (i.verb = t),
                    e.forEach(function (e2) {
                      e2.sseEvent
                        ? Be(n, t, r, e2.sseEvent)
                        : e2.trigger === 'revealed'
                        ? (De(), Fe(n))
                        : e2.trigger === 'load'
                        ? Ze(n, t, r, i, e2.delay)
                        : e2.pollInterval
                        ? ((i.polling = !0), Le(n, t, r, e2.pollInterval))
                        : Ie(n, t, r, i, e2);
                    });
                }
              }),
              o
            );
          }
          function Ye(e) {
            if (e.type === 'text/javascript' || e.type === '')
              try {
                Ut(e, function () {
                  Function(e.innerText)();
                });
              } catch (e2) {
                ut(e2);
              }
          }
          function Ke(e) {
            d(e, 'script') && Ye(e),
              X(E(e, 'script'), function (e2) {
                Ye(e2);
              });
          }
          function Qe() {
            return document.querySelector('[hx-boost], [data-hx-boost]');
          }
          function et(e) {
            if (e.querySelectorAll) {
              var t = Qe() ? ', a, form' : '',
                r = e.querySelectorAll(
                  n + t + ', [hx-sse], [data-hx-sse], [hx-ws], [data-hx-ws]'
                );
              return r;
            } else return [];
          }
          function tt(e) {
            if (!(e.closest && e.closest(v.config.disableSelector))) {
              var t = F(e);
              if (!t.initialized) {
                (t.initialized = !0),
                  lt(e, 'htmx:beforeProcessNode'),
                  e.value && (t.lastValue = e.value);
                var r = Oe(e),
                  n = Ge(e, t, r);
                !n && k(e, 'hx-boost') === 'true' && Te(e, t, r);
                var i = I(e, 'hx-sse');
                i && Ve(e, t, i);
                var o = I(e, 'hx-ws');
                o && Xe(e, t, o), lt(e, 'htmx:afterProcessNode');
              }
            }
          }
          function rt(e) {
            (e = N(e)),
              tt(e),
              X(et(e), function (e2) {
                tt(e2);
              });
          }
          function nt(e) {
            return e.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase();
          }
          function it(e, t) {
            var r;
            return (
              window.CustomEvent && typeof window.CustomEvent == 'function'
                ? (r = new CustomEvent(e, { bubbles: !0, cancelable: !0, detail: t }))
                : ((r = M().createEvent('CustomEvent')),
                  r.initCustomEvent(e, !0, !0, t)),
              r
            );
          }
          function ot(e, t, r) {
            lt(e, t, U({ error: t }, r));
          }
          function at(e) {
            return e === 'htmx:afterProcessNode';
          }
          function st(e, t) {
            X(er(e), function (e2) {
              try {
                t(e2);
              } catch (e3) {
                ut(e3);
              }
            });
          }
          function ut(e) {
            console.error ? console.error(e) : console.log && console.log('ERROR: ', e);
          }
          function lt(e, t, r) {
            (e = N(e)), r == null && (r = {}), (r.elt = e);
            var n = it(t, r);
            v.logger && !at(t) && v.logger(e, t, r),
              r.error && (ut(r.error), lt(e, 'htmx:error', { errorInfo: r }));
            var i = e.dispatchEvent(n),
              o = nt(t);
            if (i && o !== t) {
              var a = it(o, n.detail);
              i = i && e.dispatchEvent(a);
            }
            return (
              st(e, function (e2) {
                i = i && e2.onEvent(t, n) !== !1;
              }),
              i
            );
          }
          var ft = null;
          function ct() {
            var e = M().querySelector('[hx-history-elt],[data-hx-history-elt]');
            return e || M().body;
          }
          function ht(e, t, r, n) {
            for (
              var i = x(localStorage.getItem('htmx-history-cache')) || [], o = 0;
              o < i.length;
              o++
            )
              if (i[o].url === e) {
                i.splice(o, 1);
                break;
              }
            for (
              i.push({ url: e, content: t, title: r, scroll: n });
              i.length > v.config.historyCacheSize;

            )
              i.shift();
            for (; i.length > 0; )
              try {
                localStorage.setItem('htmx-history-cache', JSON.stringify(i));
                break;
              } catch (e2) {
                ot(M().body, 'htmx:historyCacheError', { cause: e2, cache: i }),
                  i.shift();
              }
          }
          function dt(e) {
            for (
              var t = x(localStorage.getItem('htmx-history-cache')) || [], r = 0;
              r < t.length;
              r++
            )
              if (t[r].url === e) return t[r];
            return null;
          }
          function vt(e) {
            var t = v.config.requestClass,
              r = e.cloneNode(!0);
            return (
              X(E(r, '.' + t), function (e2) {
                A(e2, t);
              }),
              r.innerHTML
            );
          }
          function gt() {
            var e = ct(),
              t = ft || location.pathname + location.search;
            lt(M().body, 'htmx:beforeHistorySave', { path: t, historyElt: e }),
              v.config.historyEnabled &&
                history.replaceState({ htmx: !0 }, M().title, window.location.href),
              ht(t, vt(e), M().title, window.scrollY);
          }
          function pt(e) {
            v.config.historyEnabled && history.pushState({ htmx: !0 }, '', e), (ft = e);
          }
          function mt(e) {
            X(e, function (e2) {
              e2.call();
            });
          }
          function yt(n) {
            var e = new XMLHttpRequest(),
              i = { path: n, xhr: e };
            lt(M().body, 'htmx:historyCacheMiss', i),
              e.open('GET', n, !0),
              e.setRequestHeader('HX-History-Restore-Request', 'true'),
              (e.onload = function () {
                if (this.status >= 200 && this.status < 400) {
                  lt(M().body, 'htmx:historyCacheMissLoad', i);
                  var e2 = u(this.response);
                  e2 = e2.querySelector('[hx-history-elt],[data-hx-history-elt]') || e2;
                  var t = ct(),
                    r = Ft(t);
                  se(t, e2, r),
                    mt(r.tasks),
                    (ft = n),
                    lt(M().body, 'htmx:historyRestore', { path: n });
                } else ot(M().body, 'htmx:historyCacheMissLoadError', i);
              }),
              e.send();
          }
          function xt(e) {
            gt(), (e = e || location.pathname + location.search);
            var t = dt(e);
            if (t) {
              var r = u(t.content),
                n = ct(),
                i = Ft(n);
              se(n, r, i),
                mt(i.tasks),
                (document.title = t.title),
                window.scrollTo(0, t.scroll),
                (ft = e),
                lt(M().body, 'htmx:historyRestore', { path: e });
            } else v.config.refreshOnHistoryMiss ? window.location.reload(!0) : yt(e);
          }
          function bt(e) {
            var t = k(e, 'hx-push-url');
            return (t && t !== 'false') || (e.tagName === 'A' && F(e).boosted);
          }
          function wt(e) {
            var t = k(e, 'hx-push-url');
            return t === 'true' || t === 'false' ? null : t;
          }
          function St(e) {
            var t = k(e, 'hx-indicator');
            if (t) var r = q(e, t);
            else r = [e];
            return (
              X(r, function (e2) {
                e2.classList.add.call(e2.classList, v.config.requestClass);
              }),
              r
            );
          }
          function Et(e) {
            X(e, function (e2) {
              e2.classList.remove.call(e2.classList, v.config.requestClass);
            });
          }
          function Ct(e, t) {
            for (var r = 0; r < e.length; r++) {
              var n = e[r];
              if (n.isSameNode(t)) return !0;
            }
            return !1;
          }
          function Ot(e) {
            return e.name === '' ||
              e.name == null ||
              e.disabled ||
              e.type === 'button' ||
              e.type === 'submit' ||
              e.tagName === 'image' ||
              e.tagName === 'reset' ||
              e.tagName === 'file'
              ? !1
              : e.type === 'checkbox' || e.type === 'radio'
              ? e.checked
              : !0;
          }
          function At(t, r, n, e, i) {
            if (!(e == null || Ct(t, e))) {
              if ((t.push(e), Ot(e))) {
                var o = l(e, 'name'),
                  a = e.value;
                if (
                  (e.multiple &&
                    (a = p(e.querySelectorAll('option:checked')).map(function (e2) {
                      return e2.value;
                    })),
                  e.files && (a = p(e.files)),
                  o != null && a != null)
                ) {
                  var s = r[o];
                  s
                    ? Array.isArray(s)
                      ? Array.isArray(a)
                        ? (r[o] = s.concat(a))
                        : s.push(a)
                      : Array.isArray(a)
                      ? (r[o] = [s].concat(a))
                      : (r[o] = [s, a])
                    : (r[o] = a);
                }
                i && Lt(e, n);
              }
              if (d(e, 'form')) {
                var u = e.elements;
                X(u, function (e2) {
                  At(t, r, n, e2, i);
                });
              }
            }
          }
          function Lt(e, t) {
            e.willValidate &&
              (lt(e, 'htmx:validation:validate'),
              e.checkValidity() ||
                (t.push({ elt: e, message: e.validationMessage, validity: e.validity }),
                lt(e, 'htmx:validation:failed', {
                  message: e.validationMessage,
                  validity: e.validity,
                })));
          }
          function Rt(e, t) {
            var r = [],
              n = {},
              i = {},
              o = [],
              a = d(e, 'form') && e.noValidate !== !0;
            t !== 'get' && At(r, i, o, T(e, 'form'), a), At(r, n, o, e, a);
            var s = k(e, 'hx-include');
            if (s) {
              var u = q(e, s);
              X(u, function (e2) {
                At(r, n, o, e2, a),
                  d(e2, 'form') ||
                    X(e2.querySelectorAll(Ce), function (e3) {
                      At(r, n, o, e3, a);
                    });
              });
            }
            return (n = U(n, i)), { errors: o, values: n };
          }
          function Tt(e, t, r) {
            return (
              e !== '' && (e += '&'),
              (e += encodeURIComponent(t) + '=' + encodeURIComponent(r)),
              e
            );
          }
          function qt(e) {
            var t = '';
            for (var r in e)
              if (e.hasOwnProperty(r)) {
                var n = e[r];
                Array.isArray(n)
                  ? X(n, function (e2) {
                      t = Tt(t, r, e2);
                    })
                  : (t = Tt(t, r, n));
              }
            return t;
          }
          function Ht(e) {
            var t = new FormData();
            for (var r in e)
              if (e.hasOwnProperty(r)) {
                var n = e[r];
                Array.isArray(n)
                  ? X(n, function (e2) {
                      t.append(r, e2);
                    })
                  : t.append(r, n);
              }
            return t;
          }
          function Nt(e, t, r) {
            var n = {
              'HX-Request': 'true',
              'HX-Trigger': l(e, 'id'),
              'HX-Trigger-Name': l(e, 'name'),
              'HX-Target': I(t, 'id'),
              'HX-Current-URL': M().location.href,
            };
            return Pt(e, 'hx-headers', !1, n), r !== void 0 && (n['HX-Prompt'] = r), n;
          }
          function It(t, e) {
            var r = k(e, 'hx-params');
            if (r) {
              if (r === 'none') return {};
              if (r === '*') return t;
              if (r.indexOf('not ') === 0)
                return (
                  X(r.substr(4).split(','), function (e2) {
                    (e2 = e2.trim()), delete t[e2];
                  }),
                  t
                );
              var n = {};
              return (
                X(r.split(','), function (e2) {
                  (e2 = e2.trim()), (n[e2] = t[e2]);
                }),
                n
              );
            } else return t;
          }
          function Mt(e) {
            return l(e, 'href') && l(e, 'href').indexOf('#') >= 0;
          }
          function kt(e) {
            var t = k(e, 'hx-swap'),
              r = {
                swapStyle: F(e).boosted ? 'innerHTML' : v.config.defaultSwapStyle,
                swapDelay: v.config.defaultSwapDelay,
                settleDelay: v.config.defaultSettleDelay,
              };
            if ((F(e).boosted && !Mt(e) && (r.show = 'top'), t)) {
              var n = y(t);
              if (n.length > 0) {
                r.swapStyle = n[0];
                for (var i = 1; i < n.length; i++) {
                  var o = n[i];
                  o.indexOf('swap:') === 0 && (r.swapDelay = f(o.substr(5))),
                    o.indexOf('settle:') === 0 && (r.settleDelay = f(o.substr(7))),
                    o.indexOf('scroll:') === 0 && (r.scroll = o.substr(7)),
                    o.indexOf('show:') === 0 && (r.show = o.substr(5));
                }
              }
            }
            return r;
          }
          function Dt(t, r, n) {
            var i = null;
            return (
              st(r, function (e) {
                i == null && (i = e.encodeParameters(t, n, r));
              }),
              i ?? (k(r, 'hx-encoding') === 'multipart/form-data' ? Ht(n) : qt(n))
            );
          }
          function Ft(e) {
            return { tasks: [], elts: [e] };
          }
          function Xt(e, t) {
            var r = e[0],
              n = e[e.length - 1];
            t.scroll &&
              (t.scroll === 'top' && r && (r.scrollTop = 0),
              t.scroll === 'bottom' && n && (n.scrollTop = n.scrollHeight)),
              t.show &&
                (t.show === 'top' && r && r.scrollIntoView(!0),
                t.show === 'bottom' && n && n.scrollIntoView(!1));
          }
          function Pt(e, t, r, n) {
            if ((n == null && (n = {}), e == null)) return n;
            var i = I(e, t);
            if (i) {
              var o = i.trim(),
                a = r;
              o.indexOf('javascript:') === 0 && ((o = o.substr(11)), (a = !0)),
                o.indexOf('{') !== 0 && (o = '{' + o + '}');
              var s;
              a
                ? (s = Ut(
                    e,
                    function () {
                      return Function('return (' + o + ')')();
                    },
                    {}
                  ))
                : (s = x(o));
              for (var u in s) s.hasOwnProperty(u) && n[u] == null && (n[u] = s[u]);
            }
            return Pt(c(e), t, r, n);
          }
          function Ut(e, t, r) {
            return v.config.allowEval ? t() : (ot(e, 'htmx:evalDisallowedError'), r);
          }
          function jt(e, t) {
            return Pt(e, 'hx-vars', !0, t);
          }
          function zt(e, t) {
            return Pt(e, 'hx-vals', !1, t);
          }
          function Vt(e) {
            return U(jt(e), zt(e));
          }
          function Wt(t, r, n) {
            if (n !== null)
              try {
                t.setRequestHeader(r, n);
              } catch (e) {
                t.setRequestHeader(r, encodeURIComponent(n)),
                  t.setRequestHeader(r + '-URI-AutoEncoded', 'true');
              }
          }
          function _t(t) {
            if (t.responseURL && typeof URL != 'undefined')
              try {
                var e = new URL(t.responseURL);
                return e.pathname + e.search;
              } catch (e2) {
                ot(M().body, 'htmx:badResponseUrl', { url: t.responseURL });
              }
          }
          function Bt(e, t) {
            return e.getAllResponseHeaders().match(t);
          }
          function $t(e, t, r) {
            return r
              ? r instanceof Element || o(r, 'String')
                ? Jt(e, t, null, null, { targetOverride: N(r) })
                : Jt(e, t, N(r.source), r.event, {
                    handler: r.handler,
                    headers: r.headers,
                    values: r.values,
                    targetOverride: N(r.target),
                  })
              : Jt(e, t);
          }
          function Jt(e, t, r, n, i) {
            var o = null,
              a = null;
            if (((i = i ?? {}), typeof Promise != 'undefined'))
              var s = new Promise(function (e2, t2) {
                (o = e2), (a = t2);
              });
            r == null && (r = M().body);
            var u = i.handler || Zt;
            if (!!P(r)) {
              var l = i.targetOverride || W(r);
              if (l == null) {
                ot(r, 'htmx:targetError', { target: I(r, 'hx-target') });
                return;
              }
              var f = F(r);
              if (f.requestInFlight) {
                f.queuedRequest = function () {
                  Jt(e, t, r, n);
                };
                return;
              } else f.requestInFlight = !0;
              var c = function () {
                  f.requestInFlight = !1;
                  var e2 = f.queuedRequest;
                  (f.queuedRequest = null), e2 && e2();
                },
                h = k(r, 'hx-prompt');
              if (h) {
                var d = prompt(h);
                return (
                  (d === null || !lt(r, 'htmx:prompt', { prompt: d, target: l })) &&
                    D(o),
                  c(),
                  s
                );
              }
              var v = k(r, 'hx-confirm');
              if (v && !confirm(v)) return D(o), c(), s;
              var g = new XMLHttpRequest(),
                p = Nt(r, l, d);
              i.headers && (p = U(p, i.values));
              var m = Rt(r, e),
                y = m.errors,
                x = m.values;
              i.values && (x = U(x, i.values));
              var b = Vt(r),
                w = U(x, b),
                S = It(w, r);
              e !== 'get' &&
                k(r, 'hx-encoding') == null &&
                (p['Content-Type'] =
                  'application/x-www-form-urlencoded; charset=UTF-8'),
                (t == null || t === '') && (t = M().location.href);
              var E = {
                parameters: S,
                unfilteredParameters: w,
                headers: p,
                target: l,
                verb: e,
                errors: y,
                path: t,
                triggeringEvent: n,
              };
              if (!lt(r, 'htmx:configRequest', E)) return c();
              if (
                ((t = E.path),
                (e = E.verb),
                (p = E.headers),
                (S = E.parameters),
                (y = E.errors),
                y && y.length > 0)
              )
                return lt(r, 'htmx:validation:halted', E), D(o), c(), s;
              var C = t.split('#'),
                O = C[0],
                A = C[1];
              if (e === 'get') {
                var L = O,
                  R = Object.keys(S).length !== 0;
                R &&
                  (L.indexOf('?') < 0 ? (L += '?') : (L += '&'),
                  (L += qt(S)),
                  A && (L += '#' + A)),
                  g.open('GET', L, !0);
              } else g.open(e.toUpperCase(), t, !0);
              g.overrideMimeType('text/html');
              for (var T in p)
                if (p.hasOwnProperty(T)) {
                  var q = p[T];
                  Wt(g, T, q);
                }
              var H = {
                xhr: g,
                target: l,
                requestConfig: E,
                pathInfo: { path: t, finalPath: L, anchor: A },
              };
              if (
                ((g.onload = function () {
                  try {
                    u(r, H);
                  } catch (e3) {
                    throw (ot(r, 'htmx:onLoadError', U({ error: e3 }, H)), e3);
                  } finally {
                    Et(N);
                    var e2 = r;
                    P(r) || (e2 = F(l).replacedWith || l),
                      lt(e2, 'htmx:afterRequest', H),
                      lt(e2, 'htmx:afterOnLoad', H),
                      D(o),
                      c();
                  }
                }),
                (g.onerror = function () {
                  Et(N);
                  var e2 = r;
                  P(r) || (e2 = F(l).replacedWith || l),
                    ot(e2, 'htmx:afterRequest', H),
                    ot(e2, 'htmx:sendError', H),
                    D(a),
                    c();
                }),
                (g.onabort = function () {
                  Et(N);
                  var e2 = r;
                  P(r) || (e2 = F(l).replacedWith || l),
                    ot(e2, 'htmx:afterRequest', H),
                    ot(e2, 'htmx:sendAbort', H),
                    D(a),
                    c();
                }),
                !lt(r, 'htmx:beforeRequest', H))
              )
                return D(o), c(), s;
              var N = St(r);
              return (
                X(['loadstart', 'loadend', 'progress', 'abort'], function (t2) {
                  X([g, g.upload], function (e2) {
                    e2.addEventListener(t2, function (e3) {
                      lt(r, 'htmx:xhr:' + t2, {
                        lengthComputable: e3.lengthComputable,
                        loaded: e3.loaded,
                        total: e3.total,
                      });
                    });
                  });
                }),
                lt(r, 'htmx:beforeSend', H),
                g.send(e === 'get' ? null : Dt(g, r, S)),
                s
              );
            }
          }
          function Zt(a, s) {
            var u = s.xhr,
              l = s.target;
            if (!!lt(a, 'htmx:beforeOnLoad', s)) {
              if ((Bt(u, /HX-Trigger:/i) && de(u, 'HX-Trigger', a), Bt(u, /HX-Push:/i)))
                var f = u.getResponseHeader('HX-Push');
              if (Bt(u, /HX-Redirect:/i)) {
                window.location.href = u.getResponseHeader('HX-Redirect');
                return;
              }
              if (
                Bt(u, /HX-Refresh:/i) &&
                u.getResponseHeader('HX-Refresh') === 'true'
              ) {
                location.reload();
                return;
              }
              var c = bt(a) || f;
              if (u.status >= 200 && u.status < 400) {
                if ((u.status === 286 && Ae(a), u.status !== 204)) {
                  if (!lt(l, 'htmx:beforeSwap', s)) return;
                  var h = u.response;
                  st(a, function (e2) {
                    h = e2.transformResponse(h, u, a);
                  }),
                    c && gt();
                  var d = kt(a);
                  l.classList.add(v.config.swappingClass);
                  var e = function () {
                    try {
                      var e2 = document.activeElement,
                        t = {
                          elt: e2,
                          start: e2 ? e2.selectionStart : null,
                          end: e2 ? e2.selectionEnd : null,
                        },
                        r = Ft(l);
                      if (
                        (he(d.swapStyle, l, a, h, r), t.elt && !P(t.elt) && t.elt.id)
                      ) {
                        var n = document.getElementById(t.elt.id);
                        n &&
                          (t.start &&
                            n.setSelectionRange &&
                            n.setSelectionRange(t.start, t.end),
                          n.focus());
                      }
                      if (
                        (l.classList.remove(v.config.swappingClass),
                        X(r.elts, function (e3) {
                          e3.classList && e3.classList.add(v.config.settlingClass),
                            lt(e3, 'htmx:afterSwap', s);
                        }),
                        s.pathInfo.anchor && (location.hash = s.pathInfo.anchor),
                        Bt(u, /HX-Trigger-After-Swap:/i))
                      ) {
                        var i = a;
                        P(a) || (i = M().body), de(u, 'HX-Trigger-After-Swap', i);
                      }
                      var o = function () {
                        if (
                          (X(r.tasks, function (e4) {
                            e4.call();
                          }),
                          X(r.elts, function (e4) {
                            e4.classList && e4.classList.remove(v.config.settlingClass),
                              lt(e4, 'htmx:afterSettle', s);
                          }),
                          c)
                        ) {
                          var e3 =
                            f ||
                            wt(a) ||
                            _t(u) ||
                            s.pathInfo.finalPath ||
                            s.pathInfo.path;
                          pt(e3), lt(M().body, 'htmx:pushedIntoHistory', { path: e3 });
                        }
                        if ((Xt(r.elts, d), Bt(u, /HX-Trigger-After-Settle:/i))) {
                          var t2 = a;
                          P(a) || (t2 = M().body), de(u, 'HX-Trigger-After-Settle', t2);
                        }
                      };
                      d.settleDelay > 0 ? setTimeout(o, d.settleDelay) : o();
                    } catch (e3) {
                      throw (ot(a, 'htmx:swapError', s), e3);
                    }
                  };
                  d.swapDelay > 0 ? setTimeout(e, d.swapDelay) : e();
                }
              } else
                ot(
                  a,
                  'htmx:responseError',
                  U(
                    {
                      error:
                        'Response Status Error Code ' +
                        u.status +
                        ' from ' +
                        s.pathInfo.path,
                    },
                    s
                  )
                );
            }
          }
          var Gt = {};
          function Yt() {
            return {
              onEvent: function (e, t) {
                return !0;
              },
              transformResponse: function (e, t, r) {
                return e;
              },
              isInlineSwap: function (e) {
                return !1;
              },
              handleSwap: function (e, t, r, n) {
                return !1;
              },
              encodeParameters: function (e, t, r) {
                return null;
              },
            };
          }
          function Kt(e, t) {
            Gt[e] = U(Yt(), t);
          }
          function Qt(e) {
            delete Gt[e];
          }
          function er(e, r, n) {
            if (e == null) return r;
            r == null && (r = []), n == null && (n = []);
            var t = I(e, 'hx-ext');
            return (
              t &&
                X(t.split(','), function (e2) {
                  if (((e2 = e2.replace(/ /g, '')), e2.slice(0, 7) == 'ignore:')) {
                    n.push(e2.slice(7));
                    return;
                  }
                  if (n.indexOf(e2) < 0) {
                    var t2 = Gt[e2];
                    t2 && r.indexOf(t2) < 0 && r.push(t2);
                  }
                }),
              er(c(e), r, n)
            );
          }
          function tr(e) {
            M().readyState !== 'loading'
              ? e()
              : M().addEventListener('DOMContentLoaded', e);
          }
          function rr() {
            v.config.includeIndicatorStyles !== !1 &&
              M().head.insertAdjacentHTML(
                'beforeend',
                '<style>                      .' +
                  v.config.indicatorClass +
                  '{opacity:0;transition: opacity 200ms ease-in;}                      .' +
                  v.config.requestClass +
                  ' .' +
                  v.config.indicatorClass +
                  '{opacity:1}                      .' +
                  v.config.requestClass +
                  '.' +
                  v.config.indicatorClass +
                  '{opacity:1}                    </style>'
              );
          }
          function nr() {
            var e = M().querySelector('meta[name="htmx-config"]');
            return e ? x(e.content) : null;
          }
          function ir() {
            var e = nr();
            e && (v.config = U(v.config, e));
          }
          return (
            tr(function () {
              ir(), rr();
              var e = M().body;
              rt(e),
                (window.onpopstate = function (e2) {
                  e2.state && e2.state.htmx && xt();
                }),
                setTimeout(function () {
                  lt(e, 'htmx:load', {});
                }, 0);
            }),
            v
          );
        })();
      });
    },
  });
  var import_alpinejs = __toModule(require_alpine()),
    import_htmx = __toModule(require_htmx_min());
  function _typeof(obj) {
    return (
      typeof Symbol == 'function' && typeof Symbol.iterator == 'symbol'
        ? (_typeof = function (obj2) {
            return typeof obj2;
          })
        : (_typeof = function (obj2) {
            return obj2 &&
              typeof Symbol == 'function' &&
              obj2.constructor === Symbol &&
              obj2 !== Symbol.prototype
              ? 'symbol'
              : typeof obj2;
          }),
      _typeof(obj)
    );
  }
  function _defineProperty(obj, key, value) {
    return (
      key in obj
        ? Object.defineProperty(obj, key, {
            value,
            enumerable: !0,
            configurable: !0,
            writable: !0,
          })
        : (obj[key] = value),
      obj
    );
  }
  function _extends() {
    return (
      (_extends =
        Object.assign ||
        function (target) {
          for (var i = 1; i < arguments.length; i++) {
            var source = arguments[i];
            for (var key in source)
              Object.prototype.hasOwnProperty.call(source, key) &&
                (target[key] = source[key]);
          }
          return target;
        }),
      _extends.apply(this, arguments)
    );
  }
  function _objectSpread(target) {
    for (var i = 1; i < arguments.length; i++) {
      var source = arguments[i] != null ? arguments[i] : {},
        ownKeys = Object.keys(source);
      typeof Object.getOwnPropertySymbols == 'function' &&
        (ownKeys = ownKeys.concat(
          Object.getOwnPropertySymbols(source).filter(function (sym) {
            return Object.getOwnPropertyDescriptor(source, sym).enumerable;
          })
        )),
        ownKeys.forEach(function (key) {
          _defineProperty(target, key, source[key]);
        });
    }
    return target;
  }
  function _objectWithoutPropertiesLoose(source, excluded) {
    if (source == null) return {};
    var target = {},
      sourceKeys = Object.keys(source),
      key,
      i;
    for (i = 0; i < sourceKeys.length; i++)
      (key = sourceKeys[i]),
        !(excluded.indexOf(key) >= 0) && (target[key] = source[key]);
    return target;
  }
  function _objectWithoutProperties(source, excluded) {
    if (source == null) return {};
    var target = _objectWithoutPropertiesLoose(source, excluded),
      key,
      i;
    if (Object.getOwnPropertySymbols) {
      var sourceSymbolKeys = Object.getOwnPropertySymbols(source);
      for (i = 0; i < sourceSymbolKeys.length; i++)
        (key = sourceSymbolKeys[i]),
          !(excluded.indexOf(key) >= 0) &&
            (!Object.prototype.propertyIsEnumerable.call(source, key) ||
              (target[key] = source[key]));
    }
    return target;
  }
  var version = '1.13.0';
  function userAgent(pattern) {
    if (typeof window != 'undefined' && window.navigator)
      return !!navigator.userAgent.match(pattern);
  }
  var IE11OrLess = userAgent(/(?:Trident.*rv[ :]?11\.|msie|iemobile|Windows Phone)/i),
    Edge = userAgent(/Edge/i),
    FireFox = userAgent(/firefox/i),
    Safari = userAgent(/safari/i) && !userAgent(/chrome/i) && !userAgent(/android/i),
    IOS = userAgent(/iP(ad|od|hone)/i),
    ChromeForAndroid = userAgent(/chrome/i) && userAgent(/android/i),
    captureMode = { capture: !1, passive: !1 };
  function on(el, event, fn) {
    el.addEventListener(event, fn, !IE11OrLess && captureMode);
  }
  function off(el, event, fn) {
    el.removeEventListener(event, fn, !IE11OrLess && captureMode);
  }
  function matches(el, selector) {
    if (!!selector) {
      if ((selector[0] === '>' && (selector = selector.substring(1)), el))
        try {
          if (el.matches) return el.matches(selector);
          if (el.msMatchesSelector) return el.msMatchesSelector(selector);
          if (el.webkitMatchesSelector) return el.webkitMatchesSelector(selector);
        } catch (_) {
          return !1;
        }
      return !1;
    }
  }
  function getParentOrHost(el) {
    return el.host && el !== document && el.host.nodeType ? el.host : el.parentNode;
  }
  function closest(el, selector, ctx, includeCTX) {
    if (el) {
      ctx = ctx || document;
      do {
        if (
          (selector != null &&
            (selector[0] === '>'
              ? el.parentNode === ctx && matches(el, selector)
              : matches(el, selector))) ||
          (includeCTX && el === ctx)
        )
          return el;
        if (el === ctx) break;
      } while ((el = getParentOrHost(el)));
    }
    return null;
  }
  var R_SPACE = /\s+/g;
  function toggleClass(el, name, state) {
    if (el && name)
      if (el.classList) el.classList[state ? 'add' : 'remove'](name);
      else {
        var className = (' ' + el.className + ' ')
          .replace(R_SPACE, ' ')
          .replace(' ' + name + ' ', ' ');
        el.className = (className + (state ? ' ' + name : '')).replace(R_SPACE, ' ');
      }
  }
  function css(el, prop, val) {
    var style = el && el.style;
    if (style) {
      if (val === void 0)
        return (
          document.defaultView && document.defaultView.getComputedStyle
            ? (val = document.defaultView.getComputedStyle(el, ''))
            : el.currentStyle && (val = el.currentStyle),
          prop === void 0 ? val : val[prop]
        );
      !(prop in style) && prop.indexOf('webkit') === -1 && (prop = '-webkit-' + prop),
        (style[prop] = val + (typeof val == 'string' ? '' : 'px'));
    }
  }
  function matrix(el, selfOnly) {
    var appliedTransforms = '';
    if (typeof el == 'string') appliedTransforms = el;
    else
      do {
        var transform = css(el, 'transform');
        transform &&
          transform !== 'none' &&
          (appliedTransforms = transform + ' ' + appliedTransforms);
      } while (!selfOnly && (el = el.parentNode));
    var matrixFn =
      window.DOMMatrix ||
      window.WebKitCSSMatrix ||
      window.CSSMatrix ||
      window.MSCSSMatrix;
    return matrixFn && new matrixFn(appliedTransforms);
  }
  function find(ctx, tagName, iterator) {
    if (ctx) {
      var list = ctx.getElementsByTagName(tagName),
        i = 0,
        n = list.length;
      if (iterator) for (; i < n; i++) iterator(list[i], i);
      return list;
    }
    return [];
  }
  function getWindowScrollingElement() {
    var scrollingElement = document.scrollingElement;
    return scrollingElement || document.documentElement;
  }
  function getRect(
    el,
    relativeToContainingBlock,
    relativeToNonStaticParent,
    undoScale,
    container
  ) {
    if (!(!el.getBoundingClientRect && el !== window)) {
      var elRect, top, left, bottom, right, height, width;
      if (
        (el !== window && el.parentNode && el !== getWindowScrollingElement()
          ? ((elRect = el.getBoundingClientRect()),
            (top = elRect.top),
            (left = elRect.left),
            (bottom = elRect.bottom),
            (right = elRect.right),
            (height = elRect.height),
            (width = elRect.width))
          : ((top = 0),
            (left = 0),
            (bottom = window.innerHeight),
            (right = window.innerWidth),
            (height = window.innerHeight),
            (width = window.innerWidth)),
        (relativeToContainingBlock || relativeToNonStaticParent) &&
          el !== window &&
          ((container = container || el.parentNode), !IE11OrLess))
      )
        do
          if (
            container &&
            container.getBoundingClientRect &&
            (css(container, 'transform') !== 'none' ||
              (relativeToNonStaticParent && css(container, 'position') !== 'static'))
          ) {
            var containerRect = container.getBoundingClientRect();
            (top -= containerRect.top + parseInt(css(container, 'border-top-width'))),
              (left -=
                containerRect.left + parseInt(css(container, 'border-left-width'))),
              (bottom = top + elRect.height),
              (right = left + elRect.width);
            break;
          }
        while ((container = container.parentNode));
      if (undoScale && el !== window) {
        var elMatrix = matrix(container || el),
          scaleX = elMatrix && elMatrix.a,
          scaleY = elMatrix && elMatrix.d;
        elMatrix &&
          ((top /= scaleY),
          (left /= scaleX),
          (width /= scaleX),
          (height /= scaleY),
          (bottom = top + height),
          (right = left + width));
      }
      return { top, left, bottom, right, width, height };
    }
  }
  function isScrolledPast(el, elSide, parentSide) {
    for (
      var parent = getParentAutoScrollElement(el, !0), elSideVal = getRect(el)[elSide];
      parent;

    ) {
      var parentSideVal = getRect(parent)[parentSide],
        visible = void 0;
      if (
        (parentSide === 'top' || parentSide === 'left'
          ? (visible = elSideVal >= parentSideVal)
          : (visible = elSideVal <= parentSideVal),
        !visible)
      )
        return parent;
      if (parent === getWindowScrollingElement()) break;
      parent = getParentAutoScrollElement(parent, !1);
    }
    return !1;
  }
  function getChild(el, childNum, options) {
    for (var currentChild = 0, i = 0, children = el.children; i < children.length; ) {
      if (
        children[i].style.display !== 'none' &&
        children[i] !== Sortable.ghost &&
        children[i] !== Sortable.dragged &&
        closest(children[i], options.draggable, el, !1)
      ) {
        if (currentChild === childNum) return children[i];
        currentChild++;
      }
      i++;
    }
    return null;
  }
  function lastChild(el, selector) {
    for (
      var last = el.lastElementChild;
      last &&
      (last === Sortable.ghost ||
        css(last, 'display') === 'none' ||
        (selector && !matches(last, selector)));

    )
      last = last.previousElementSibling;
    return last || null;
  }
  function index(el, selector) {
    var index2 = 0;
    if (!el || !el.parentNode) return -1;
    for (; (el = el.previousElementSibling); )
      el.nodeName.toUpperCase() !== 'TEMPLATE' &&
        el !== Sortable.clone &&
        (!selector || matches(el, selector)) &&
        index2++;
    return index2;
  }
  function getRelativeScrollOffset(el) {
    var offsetLeft = 0,
      offsetTop = 0,
      winScroller = getWindowScrollingElement();
    if (el)
      do {
        var elMatrix = matrix(el),
          scaleX = elMatrix.a,
          scaleY = elMatrix.d;
        (offsetLeft += el.scrollLeft * scaleX), (offsetTop += el.scrollTop * scaleY);
      } while (el !== winScroller && (el = el.parentNode));
    return [offsetLeft, offsetTop];
  }
  function indexOfObject(arr, obj) {
    for (var i in arr)
      if (!!arr.hasOwnProperty(i)) {
        for (var key in obj)
          if (obj.hasOwnProperty(key) && obj[key] === arr[i][key]) return Number(i);
      }
    return -1;
  }
  function getParentAutoScrollElement(el, includeSelf) {
    if (!el || !el.getBoundingClientRect) return getWindowScrollingElement();
    var elem = el,
      gotSelf = !1;
    do
      if (
        elem.clientWidth < elem.scrollWidth ||
        elem.clientHeight < elem.scrollHeight
      ) {
        var elemCSS = css(elem);
        if (
          (elem.clientWidth < elem.scrollWidth &&
            (elemCSS.overflowX == 'auto' || elemCSS.overflowX == 'scroll')) ||
          (elem.clientHeight < elem.scrollHeight &&
            (elemCSS.overflowY == 'auto' || elemCSS.overflowY == 'scroll'))
        ) {
          if (!elem.getBoundingClientRect || elem === document.body)
            return getWindowScrollingElement();
          if (gotSelf || includeSelf) return elem;
          gotSelf = !0;
        }
      }
    while ((elem = elem.parentNode));
    return getWindowScrollingElement();
  }
  function extend(dst, src) {
    if (dst && src)
      for (var key in src) src.hasOwnProperty(key) && (dst[key] = src[key]);
    return dst;
  }
  function isRectEqual(rect1, rect2) {
    return (
      Math.round(rect1.top) === Math.round(rect2.top) &&
      Math.round(rect1.left) === Math.round(rect2.left) &&
      Math.round(rect1.height) === Math.round(rect2.height) &&
      Math.round(rect1.width) === Math.round(rect2.width)
    );
  }
  var _throttleTimeout;
  function throttle(callback, ms) {
    return function () {
      if (!_throttleTimeout) {
        var args = arguments,
          _this = this;
        args.length === 1 ? callback.call(_this, args[0]) : callback.apply(_this, args),
          (_throttleTimeout = setTimeout(function () {
            _throttleTimeout = void 0;
          }, ms));
      }
    };
  }
  function cancelThrottle() {
    clearTimeout(_throttleTimeout), (_throttleTimeout = void 0);
  }
  function scrollBy(el, x, y) {
    (el.scrollLeft += x), (el.scrollTop += y);
  }
  function clone(el) {
    var Polymer = window.Polymer,
      $ = window.jQuery || window.Zepto;
    return Polymer && Polymer.dom
      ? Polymer.dom(el).cloneNode(!0)
      : $
      ? $(el).clone(!0)[0]
      : el.cloneNode(!0);
  }
  var expando = 'Sortable' + new Date().getTime();
  function AnimationStateManager() {
    var animationStates = [],
      animationCallbackId;
    return {
      captureAnimationState: function () {
        if (((animationStates = []), !!this.options.animation)) {
          var children = [].slice.call(this.el.children);
          children.forEach(function (child) {
            if (!(css(child, 'display') === 'none' || child === Sortable.ghost)) {
              animationStates.push({ target: child, rect: getRect(child) });
              var fromRect = _objectSpread(
                {},
                animationStates[animationStates.length - 1].rect
              );
              if (child.thisAnimationDuration) {
                var childMatrix = matrix(child, !0);
                childMatrix &&
                  ((fromRect.top -= childMatrix.f), (fromRect.left -= childMatrix.e));
              }
              child.fromRect = fromRect;
            }
          });
        }
      },
      addAnimationState: function (state) {
        animationStates.push(state);
      },
      removeAnimationState: function (target) {
        animationStates.splice(indexOfObject(animationStates, { target }), 1);
      },
      animateAll: function (callback) {
        var _this = this;
        if (!this.options.animation) {
          clearTimeout(animationCallbackId),
            typeof callback == 'function' && callback();
          return;
        }
        var animating = !1,
          animationTime = 0;
        animationStates.forEach(function (state) {
          var time = 0,
            target = state.target,
            fromRect = target.fromRect,
            toRect = getRect(target),
            prevFromRect = target.prevFromRect,
            prevToRect = target.prevToRect,
            animatingRect = state.rect,
            targetMatrix = matrix(target, !0);
          targetMatrix &&
            ((toRect.top -= targetMatrix.f), (toRect.left -= targetMatrix.e)),
            (target.toRect = toRect),
            target.thisAnimationDuration &&
              isRectEqual(prevFromRect, toRect) &&
              !isRectEqual(fromRect, toRect) &&
              (animatingRect.top - toRect.top) / (animatingRect.left - toRect.left) ==
                (fromRect.top - toRect.top) / (fromRect.left - toRect.left) &&
              (time = calculateRealTime(
                animatingRect,
                prevFromRect,
                prevToRect,
                _this.options
              )),
            isRectEqual(toRect, fromRect) ||
              ((target.prevFromRect = fromRect),
              (target.prevToRect = toRect),
              time || (time = _this.options.animation),
              _this.animate(target, animatingRect, toRect, time)),
            time &&
              ((animating = !0),
              (animationTime = Math.max(animationTime, time)),
              clearTimeout(target.animationResetTimer),
              (target.animationResetTimer = setTimeout(function () {
                (target.animationTime = 0),
                  (target.prevFromRect = null),
                  (target.fromRect = null),
                  (target.prevToRect = null),
                  (target.thisAnimationDuration = null);
              }, time)),
              (target.thisAnimationDuration = time));
        }),
          clearTimeout(animationCallbackId),
          animating
            ? (animationCallbackId = setTimeout(function () {
                typeof callback == 'function' && callback();
              }, animationTime))
            : typeof callback == 'function' && callback(),
          (animationStates = []);
      },
      animate: function (target, currentRect, toRect, duration) {
        if (duration) {
          css(target, 'transition', ''), css(target, 'transform', '');
          var elMatrix = matrix(this.el),
            scaleX = elMatrix && elMatrix.a,
            scaleY = elMatrix && elMatrix.d,
            translateX = (currentRect.left - toRect.left) / (scaleX || 1),
            translateY = (currentRect.top - toRect.top) / (scaleY || 1);
          (target.animatingX = !!translateX),
            (target.animatingY = !!translateY),
            css(
              target,
              'transform',
              'translate3d(' + translateX + 'px,' + translateY + 'px,0)'
            ),
            (this.forRepaintDummy = repaint(target)),
            css(
              target,
              'transition',
              'transform ' +
                duration +
                'ms' +
                (this.options.easing ? ' ' + this.options.easing : '')
            ),
            css(target, 'transform', 'translate3d(0,0,0)'),
            typeof target.animated == 'number' && clearTimeout(target.animated),
            (target.animated = setTimeout(function () {
              css(target, 'transition', ''),
                css(target, 'transform', ''),
                (target.animated = !1),
                (target.animatingX = !1),
                (target.animatingY = !1);
            }, duration));
        }
      },
    };
  }
  function repaint(target) {
    return target.offsetWidth;
  }
  function calculateRealTime(animatingRect, fromRect, toRect, options) {
    return (
      (Math.sqrt(
        Math.pow(fromRect.top - animatingRect.top, 2) +
          Math.pow(fromRect.left - animatingRect.left, 2)
      ) /
        Math.sqrt(
          Math.pow(fromRect.top - toRect.top, 2) +
            Math.pow(fromRect.left - toRect.left, 2)
        )) *
      options.animation
    );
  }
  var plugins = [],
    defaults = { initializeByDefault: !0 },
    PluginManager = {
      mount: function (plugin) {
        for (var option2 in defaults)
          defaults.hasOwnProperty(option2) &&
            !(option2 in plugin) &&
            (plugin[option2] = defaults[option2]);
        plugins.forEach(function (p) {
          if (p.pluginName === plugin.pluginName)
            throw 'Sortable: Cannot mount plugin '.concat(
              plugin.pluginName,
              ' more than once'
            );
        }),
          plugins.push(plugin);
      },
      pluginEvent: function (eventName, sortable, evt) {
        var _this = this;
        (this.eventCanceled = !1),
          (evt.cancel = function () {
            _this.eventCanceled = !0;
          });
        var eventNameGlobal = eventName + 'Global';
        plugins.forEach(function (plugin) {
          !sortable[plugin.pluginName] ||
            (sortable[plugin.pluginName][eventNameGlobal] &&
              sortable[plugin.pluginName][eventNameGlobal](
                _objectSpread({ sortable }, evt)
              ),
            sortable.options[plugin.pluginName] &&
              sortable[plugin.pluginName][eventName] &&
              sortable[plugin.pluginName][eventName](_objectSpread({ sortable }, evt)));
        });
      },
      initializePlugins: function (sortable, el, defaults3, options) {
        plugins.forEach(function (plugin) {
          var pluginName = plugin.pluginName;
          if (!(!sortable.options[pluginName] && !plugin.initializeByDefault)) {
            var initialized = new plugin(sortable, el, sortable.options);
            (initialized.sortable = sortable),
              (initialized.options = sortable.options),
              (sortable[pluginName] = initialized),
              _extends(defaults3, initialized.defaults);
          }
        });
        for (var option2 in sortable.options)
          if (!!sortable.options.hasOwnProperty(option2)) {
            var modified = this.modifyOption(
              sortable,
              option2,
              sortable.options[option2]
            );
            typeof modified != 'undefined' && (sortable.options[option2] = modified);
          }
      },
      getEventProperties: function (name, sortable) {
        var eventProperties = {};
        return (
          plugins.forEach(function (plugin) {
            typeof plugin.eventProperties == 'function' &&
              _extends(
                eventProperties,
                plugin.eventProperties.call(sortable[plugin.pluginName], name)
              );
          }),
          eventProperties
        );
      },
      modifyOption: function (sortable, name, value) {
        var modifiedValue;
        return (
          plugins.forEach(function (plugin) {
            !sortable[plugin.pluginName] ||
              (plugin.optionListeners &&
                typeof plugin.optionListeners[name] == 'function' &&
                (modifiedValue = plugin.optionListeners[name].call(
                  sortable[plugin.pluginName],
                  value
                )));
          }),
          modifiedValue
        );
      },
    };
  function dispatchEvent(_ref) {
    var sortable = _ref.sortable,
      rootEl2 = _ref.rootEl,
      name = _ref.name,
      targetEl = _ref.targetEl,
      cloneEl2 = _ref.cloneEl,
      toEl = _ref.toEl,
      fromEl = _ref.fromEl,
      oldIndex2 = _ref.oldIndex,
      newIndex2 = _ref.newIndex,
      oldDraggableIndex2 = _ref.oldDraggableIndex,
      newDraggableIndex2 = _ref.newDraggableIndex,
      originalEvent = _ref.originalEvent,
      putSortable2 = _ref.putSortable,
      extraEventProperties = _ref.extraEventProperties;
    if (((sortable = sortable || (rootEl2 && rootEl2[expando])), !!sortable)) {
      var evt,
        options = sortable.options,
        onName = 'on' + name.charAt(0).toUpperCase() + name.substr(1);
      window.CustomEvent && !IE11OrLess && !Edge
        ? (evt = new CustomEvent(name, { bubbles: !0, cancelable: !0 }))
        : ((evt = document.createEvent('Event')), evt.initEvent(name, !0, !0)),
        (evt.to = toEl || rootEl2),
        (evt.from = fromEl || rootEl2),
        (evt.item = targetEl || rootEl2),
        (evt.clone = cloneEl2),
        (evt.oldIndex = oldIndex2),
        (evt.newIndex = newIndex2),
        (evt.oldDraggableIndex = oldDraggableIndex2),
        (evt.newDraggableIndex = newDraggableIndex2),
        (evt.originalEvent = originalEvent),
        (evt.pullMode = putSortable2 ? putSortable2.lastPutMode : void 0);
      var allEventProperties = _objectSpread(
        {},
        extraEventProperties,
        PluginManager.getEventProperties(name, sortable)
      );
      for (var option2 in allEventProperties)
        evt[option2] = allEventProperties[option2];
      rootEl2 && rootEl2.dispatchEvent(evt),
        options[onName] && options[onName].call(sortable, evt);
    }
  }
  var pluginEvent2 = function (eventName, sortable) {
    var _ref = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : {},
      originalEvent = _ref.evt,
      data = _objectWithoutProperties(_ref, ['evt']);
    PluginManager.pluginEvent.bind(Sortable)(
      eventName,
      sortable,
      _objectSpread(
        {
          dragEl,
          parentEl,
          ghostEl,
          rootEl,
          nextEl,
          lastDownEl,
          cloneEl,
          cloneHidden,
          dragStarted: moved,
          putSortable,
          activeSortable: Sortable.active,
          originalEvent,
          oldIndex,
          oldDraggableIndex,
          newIndex,
          newDraggableIndex,
          hideGhostForTarget: _hideGhostForTarget,
          unhideGhostForTarget: _unhideGhostForTarget,
          cloneNowHidden: function () {
            cloneHidden = !0;
          },
          cloneNowShown: function () {
            cloneHidden = !1;
          },
          dispatchSortableEvent: function (name) {
            _dispatchEvent({ sortable, name, originalEvent });
          },
        },
        data
      )
    );
  };
  function _dispatchEvent(info) {
    dispatchEvent(
      _objectSpread(
        {
          putSortable,
          cloneEl,
          targetEl: dragEl,
          rootEl,
          oldIndex,
          oldDraggableIndex,
          newIndex,
          newDraggableIndex,
        },
        info
      )
    );
  }
  var dragEl,
    parentEl,
    ghostEl,
    rootEl,
    nextEl,
    lastDownEl,
    cloneEl,
    cloneHidden,
    oldIndex,
    newIndex,
    oldDraggableIndex,
    newDraggableIndex,
    activeGroup,
    putSortable,
    awaitingDragStarted = !1,
    ignoreNextClick = !1,
    sortables = [],
    tapEvt,
    touchEvt,
    lastDx,
    lastDy,
    tapDistanceLeft,
    tapDistanceTop,
    moved,
    lastTarget,
    lastDirection,
    pastFirstInvertThresh = !1,
    isCircumstantialInvert = !1,
    targetMoveDistance,
    ghostRelativeParent,
    ghostRelativeParentInitialScroll = [],
    _silent = !1,
    savedInputChecked = [],
    documentExists = typeof document != 'undefined',
    PositionGhostAbsolutely = IOS,
    CSSFloatProperty = Edge || IE11OrLess ? 'cssFloat' : 'float',
    supportDraggable =
      documentExists &&
      !ChromeForAndroid &&
      !IOS &&
      'draggable' in document.createElement('div'),
    supportCssPointerEvents = (function () {
      if (!!documentExists) {
        if (IE11OrLess) return !1;
        var el = document.createElement('x');
        return (
          (el.style.cssText = 'pointer-events:auto'), el.style.pointerEvents === 'auto'
        );
      }
    })(),
    _detectDirection = function (el, options) {
      var elCSS = css(el),
        elWidth =
          parseInt(elCSS.width) -
          parseInt(elCSS.paddingLeft) -
          parseInt(elCSS.paddingRight) -
          parseInt(elCSS.borderLeftWidth) -
          parseInt(elCSS.borderRightWidth),
        child1 = getChild(el, 0, options),
        child2 = getChild(el, 1, options),
        firstChildCSS = child1 && css(child1),
        secondChildCSS = child2 && css(child2),
        firstChildWidth =
          firstChildCSS &&
          parseInt(firstChildCSS.marginLeft) +
            parseInt(firstChildCSS.marginRight) +
            getRect(child1).width,
        secondChildWidth =
          secondChildCSS &&
          parseInt(secondChildCSS.marginLeft) +
            parseInt(secondChildCSS.marginRight) +
            getRect(child2).width;
      if (elCSS.display === 'flex')
        return elCSS.flexDirection === 'column' ||
          elCSS.flexDirection === 'column-reverse'
          ? 'vertical'
          : 'horizontal';
      if (elCSS.display === 'grid')
        return elCSS.gridTemplateColumns.split(' ').length <= 1
          ? 'vertical'
          : 'horizontal';
      if (child1 && firstChildCSS.float && firstChildCSS.float !== 'none') {
        var touchingSideChild2 = firstChildCSS.float === 'left' ? 'left' : 'right';
        return child2 &&
          (secondChildCSS.clear === 'both' ||
            secondChildCSS.clear === touchingSideChild2)
          ? 'vertical'
          : 'horizontal';
      }
      return child1 &&
        (firstChildCSS.display === 'block' ||
          firstChildCSS.display === 'flex' ||
          firstChildCSS.display === 'table' ||
          firstChildCSS.display === 'grid' ||
          (firstChildWidth >= elWidth && elCSS[CSSFloatProperty] === 'none') ||
          (child2 &&
            elCSS[CSSFloatProperty] === 'none' &&
            firstChildWidth + secondChildWidth > elWidth))
        ? 'vertical'
        : 'horizontal';
    },
    _dragElInRowColumn = function (dragRect, targetRect, vertical) {
      var dragElS1Opp = vertical ? dragRect.left : dragRect.top,
        dragElS2Opp = vertical ? dragRect.right : dragRect.bottom,
        dragElOppLength = vertical ? dragRect.width : dragRect.height,
        targetS1Opp = vertical ? targetRect.left : targetRect.top,
        targetS2Opp = vertical ? targetRect.right : targetRect.bottom,
        targetOppLength = vertical ? targetRect.width : targetRect.height;
      return (
        dragElS1Opp === targetS1Opp ||
        dragElS2Opp === targetS2Opp ||
        dragElS1Opp + dragElOppLength / 2 === targetS1Opp + targetOppLength / 2
      );
    },
    _detectNearestEmptySortable = function (x, y) {
      var ret;
      return (
        sortables.some(function (sortable) {
          if (!lastChild(sortable)) {
            var rect = getRect(sortable),
              threshold = sortable[expando].options.emptyInsertThreshold,
              insideHorizontally =
                x >= rect.left - threshold && x <= rect.right + threshold,
              insideVertically =
                y >= rect.top - threshold && y <= rect.bottom + threshold;
            if (threshold && insideHorizontally && insideVertically)
              return (ret = sortable);
          }
        }),
        ret
      );
    },
    _prepareGroup = function (options) {
      function toFn(value, pull) {
        return function (to, from, dragEl2, evt) {
          var sameGroup =
            to.options.group.name &&
            from.options.group.name &&
            to.options.group.name === from.options.group.name;
          if (value == null && (pull || sameGroup)) return !0;
          if (value == null || value === !1) return !1;
          if (pull && value === 'clone') return value;
          if (typeof value == 'function')
            return toFn(value(to, from, dragEl2, evt), pull)(to, from, dragEl2, evt);
          var otherGroup = (pull ? to : from).options.group.name;
          return (
            value === !0 ||
            (typeof value == 'string' && value === otherGroup) ||
            (value.join && value.indexOf(otherGroup) > -1)
          );
        };
      }
      var group = {},
        originalGroup = options.group;
      (!originalGroup || _typeof(originalGroup) != 'object') &&
        (originalGroup = { name: originalGroup }),
        (group.name = originalGroup.name),
        (group.checkPull = toFn(originalGroup.pull, !0)),
        (group.checkPut = toFn(originalGroup.put)),
        (group.revertClone = originalGroup.revertClone),
        (options.group = group);
    },
    _hideGhostForTarget = function () {
      !supportCssPointerEvents && ghostEl && css(ghostEl, 'display', 'none');
    },
    _unhideGhostForTarget = function () {
      !supportCssPointerEvents && ghostEl && css(ghostEl, 'display', '');
    };
  documentExists &&
    document.addEventListener(
      'click',
      function (evt) {
        if (ignoreNextClick)
          return (
            evt.preventDefault(),
            evt.stopPropagation && evt.stopPropagation(),
            evt.stopImmediatePropagation && evt.stopImmediatePropagation(),
            (ignoreNextClick = !1),
            !1
          );
      },
      !0
    );
  var nearestEmptyInsertDetectEvent = function (evt) {
      if (dragEl) {
        evt = evt.touches ? evt.touches[0] : evt;
        var nearest = _detectNearestEmptySortable(evt.clientX, evt.clientY);
        if (nearest) {
          var event = {};
          for (var i in evt) evt.hasOwnProperty(i) && (event[i] = evt[i]);
          (event.target = event.rootEl = nearest),
            (event.preventDefault = void 0),
            (event.stopPropagation = void 0),
            nearest[expando]._onDragOver(event);
        }
      }
    },
    _checkOutsideTargetEl = function (evt) {
      dragEl && dragEl.parentNode[expando]._isOutsideThisEl(evt.target);
    };
  function Sortable(el, options) {
    if (!(el && el.nodeType && el.nodeType === 1))
      throw 'Sortable: `el` must be an HTMLElement, not '.concat({}.toString.call(el));
    (this.el = el),
      (this.options = options = _extends({}, options)),
      (el[expando] = this);
    var defaults3 = {
      group: null,
      sort: !0,
      disabled: !1,
      store: null,
      handle: null,
      draggable: /^[uo]l$/i.test(el.nodeName) ? '>li' : '>*',
      swapThreshold: 1,
      invertSwap: !1,
      invertedSwapThreshold: null,
      removeCloneOnHide: !0,
      direction: function () {
        return _detectDirection(el, this.options);
      },
      ghostClass: 'sortable-ghost',
      chosenClass: 'sortable-chosen',
      dragClass: 'sortable-drag',
      ignore: 'a, img',
      filter: null,
      preventOnFilter: !0,
      animation: 0,
      easing: null,
      setData: function (dataTransfer, dragEl2) {
        dataTransfer.setData('Text', dragEl2.textContent);
      },
      dropBubble: !1,
      dragoverBubble: !1,
      dataIdAttr: 'data-id',
      delay: 0,
      delayOnTouchOnly: !1,
      touchStartThreshold:
        (Number.parseInt ? Number : window).parseInt(window.devicePixelRatio, 10) || 1,
      forceFallback: !1,
      fallbackClass: 'sortable-fallback',
      fallbackOnBody: !1,
      fallbackTolerance: 0,
      fallbackOffset: { x: 0, y: 0 },
      supportPointer:
        Sortable.supportPointer !== !1 && 'PointerEvent' in window && !Safari,
      emptyInsertThreshold: 5,
    };
    PluginManager.initializePlugins(this, el, defaults3);
    for (var name in defaults3) !(name in options) && (options[name] = defaults3[name]);
    _prepareGroup(options);
    for (var fn in this)
      fn.charAt(0) === '_' &&
        typeof this[fn] == 'function' &&
        (this[fn] = this[fn].bind(this));
    (this.nativeDraggable = options.forceFallback ? !1 : supportDraggable),
      this.nativeDraggable && (this.options.touchStartThreshold = 1),
      options.supportPointer
        ? on(el, 'pointerdown', this._onTapStart)
        : (on(el, 'mousedown', this._onTapStart),
          on(el, 'touchstart', this._onTapStart)),
      this.nativeDraggable && (on(el, 'dragover', this), on(el, 'dragenter', this)),
      sortables.push(this.el),
      options.store && options.store.get && this.sort(options.store.get(this) || []),
      _extends(this, AnimationStateManager());
  }
  Sortable.prototype = {
    constructor: Sortable,
    _isOutsideThisEl: function (target) {
      !this.el.contains(target) && target !== this.el && (lastTarget = null);
    },
    _getDirection: function (evt, target) {
      return typeof this.options.direction == 'function'
        ? this.options.direction.call(this, evt, target, dragEl)
        : this.options.direction;
    },
    _onTapStart: function (evt) {
      if (!!evt.cancelable) {
        var _this = this,
          el = this.el,
          options = this.options,
          preventOnFilter = options.preventOnFilter,
          type = evt.type,
          touch =
            (evt.touches && evt.touches[0]) ||
            (evt.pointerType && evt.pointerType === 'touch' && evt),
          target = (touch || evt).target,
          originalTarget =
            (evt.target.shadowRoot &&
              ((evt.path && evt.path[0]) ||
                (evt.composedPath && evt.composedPath()[0]))) ||
            target,
          filter = options.filter;
        if (
          (_saveInputCheckedState(el),
          !dragEl &&
            !(
              (/mousedown|pointerdown/.test(type) && evt.button !== 0) ||
              options.disabled
            ) &&
            !originalTarget.isContentEditable &&
            !(
              !this.nativeDraggable &&
              Safari &&
              target &&
              target.tagName.toUpperCase() === 'SELECT'
            ) &&
            ((target = closest(target, options.draggable, el, !1)),
            !(target && target.animated) && lastDownEl !== target))
        ) {
          if (
            ((oldIndex = index(target)),
            (oldDraggableIndex = index(target, options.draggable)),
            typeof filter == 'function')
          ) {
            if (filter.call(this, evt, target, this)) {
              _dispatchEvent({
                sortable: _this,
                rootEl: originalTarget,
                name: 'filter',
                targetEl: target,
                toEl: el,
                fromEl: el,
              }),
                pluginEvent2('filter', _this, { evt }),
                preventOnFilter && evt.cancelable && evt.preventDefault();
              return;
            }
          } else if (
            filter &&
            ((filter = filter.split(',').some(function (criteria) {
              if (
                ((criteria = closest(originalTarget, criteria.trim(), el, !1)),
                criteria)
              )
                return (
                  _dispatchEvent({
                    sortable: _this,
                    rootEl: criteria,
                    name: 'filter',
                    targetEl: target,
                    fromEl: el,
                    toEl: el,
                  }),
                  pluginEvent2('filter', _this, { evt }),
                  !0
                );
            })),
            filter)
          ) {
            preventOnFilter && evt.cancelable && evt.preventDefault();
            return;
          }
          (options.handle && !closest(originalTarget, options.handle, el, !1)) ||
            this._prepareDragStart(evt, touch, target);
        }
      }
    },
    _prepareDragStart: function (evt, touch, target) {
      var _this = this,
        el = _this.el,
        options = _this.options,
        ownerDocument = el.ownerDocument,
        dragStartFn;
      if (target && !dragEl && target.parentNode === el) {
        var dragRect = getRect(target);
        if (
          ((rootEl = el),
          (dragEl = target),
          (parentEl = dragEl.parentNode),
          (nextEl = dragEl.nextSibling),
          (lastDownEl = target),
          (activeGroup = options.group),
          (Sortable.dragged = dragEl),
          (tapEvt = {
            target: dragEl,
            clientX: (touch || evt).clientX,
            clientY: (touch || evt).clientY,
          }),
          (tapDistanceLeft = tapEvt.clientX - dragRect.left),
          (tapDistanceTop = tapEvt.clientY - dragRect.top),
          (this._lastX = (touch || evt).clientX),
          (this._lastY = (touch || evt).clientY),
          (dragEl.style['will-change'] = 'all'),
          (dragStartFn = function () {
            if ((pluginEvent2('delayEnded', _this, { evt }), Sortable.eventCanceled)) {
              _this._onDrop();
              return;
            }
            _this._disableDelayedDragEvents(),
              !FireFox && _this.nativeDraggable && (dragEl.draggable = !0),
              _this._triggerDragStart(evt, touch),
              _dispatchEvent({ sortable: _this, name: 'choose', originalEvent: evt }),
              toggleClass(dragEl, options.chosenClass, !0);
          }),
          options.ignore.split(',').forEach(function (criteria) {
            find(dragEl, criteria.trim(), _disableDraggable);
          }),
          on(ownerDocument, 'dragover', nearestEmptyInsertDetectEvent),
          on(ownerDocument, 'mousemove', nearestEmptyInsertDetectEvent),
          on(ownerDocument, 'touchmove', nearestEmptyInsertDetectEvent),
          on(ownerDocument, 'mouseup', _this._onDrop),
          on(ownerDocument, 'touchend', _this._onDrop),
          on(ownerDocument, 'touchcancel', _this._onDrop),
          FireFox &&
            this.nativeDraggable &&
            ((this.options.touchStartThreshold = 4), (dragEl.draggable = !0)),
          pluginEvent2('delayStart', this, { evt }),
          options.delay &&
            (!options.delayOnTouchOnly || touch) &&
            (!this.nativeDraggable || !(Edge || IE11OrLess)))
        ) {
          if (Sortable.eventCanceled) {
            this._onDrop();
            return;
          }
          on(ownerDocument, 'mouseup', _this._disableDelayedDrag),
            on(ownerDocument, 'touchend', _this._disableDelayedDrag),
            on(ownerDocument, 'touchcancel', _this._disableDelayedDrag),
            on(ownerDocument, 'mousemove', _this._delayedDragTouchMoveHandler),
            on(ownerDocument, 'touchmove', _this._delayedDragTouchMoveHandler),
            options.supportPointer &&
              on(ownerDocument, 'pointermove', _this._delayedDragTouchMoveHandler),
            (_this._dragStartTimer = setTimeout(dragStartFn, options.delay));
        } else dragStartFn();
      }
    },
    _delayedDragTouchMoveHandler: function (e) {
      var touch = e.touches ? e.touches[0] : e;
      Math.max(
        Math.abs(touch.clientX - this._lastX),
        Math.abs(touch.clientY - this._lastY)
      ) >=
        Math.floor(
          this.options.touchStartThreshold /
            ((this.nativeDraggable && window.devicePixelRatio) || 1)
        ) && this._disableDelayedDrag();
    },
    _disableDelayedDrag: function () {
      dragEl && _disableDraggable(dragEl),
        clearTimeout(this._dragStartTimer),
        this._disableDelayedDragEvents();
    },
    _disableDelayedDragEvents: function () {
      var ownerDocument = this.el.ownerDocument;
      off(ownerDocument, 'mouseup', this._disableDelayedDrag),
        off(ownerDocument, 'touchend', this._disableDelayedDrag),
        off(ownerDocument, 'touchcancel', this._disableDelayedDrag),
        off(ownerDocument, 'mousemove', this._delayedDragTouchMoveHandler),
        off(ownerDocument, 'touchmove', this._delayedDragTouchMoveHandler),
        off(ownerDocument, 'pointermove', this._delayedDragTouchMoveHandler);
    },
    _triggerDragStart: function (evt, touch) {
      (touch = touch || (evt.pointerType == 'touch' && evt)),
        !this.nativeDraggable || touch
          ? this.options.supportPointer
            ? on(document, 'pointermove', this._onTouchMove)
            : touch
            ? on(document, 'touchmove', this._onTouchMove)
            : on(document, 'mousemove', this._onTouchMove)
          : (on(dragEl, 'dragend', this), on(rootEl, 'dragstart', this._onDragStart));
      try {
        document.selection
          ? _nextTick(function () {
              document.selection.empty();
            })
          : window.getSelection().removeAllRanges();
      } catch (err) {}
    },
    _dragStarted: function (fallback, evt) {
      if (((awaitingDragStarted = !1), rootEl && dragEl)) {
        pluginEvent2('dragStarted', this, { evt }),
          this.nativeDraggable && on(document, 'dragover', _checkOutsideTargetEl);
        var options = this.options;
        !fallback && toggleClass(dragEl, options.dragClass, !1),
          toggleClass(dragEl, options.ghostClass, !0),
          (Sortable.active = this),
          fallback && this._appendGhost(),
          _dispatchEvent({ sortable: this, name: 'start', originalEvent: evt });
      } else this._nulling();
    },
    _emulateDragOver: function () {
      if (touchEvt) {
        (this._lastX = touchEvt.clientX),
          (this._lastY = touchEvt.clientY),
          _hideGhostForTarget();
        for (
          var target = document.elementFromPoint(touchEvt.clientX, touchEvt.clientY),
            parent = target;
          target &&
          target.shadowRoot &&
          ((target = target.shadowRoot.elementFromPoint(
            touchEvt.clientX,
            touchEvt.clientY
          )),
          target !== parent);

        )
          parent = target;
        if ((dragEl.parentNode[expando]._isOutsideThisEl(target), parent))
          do {
            if (parent[expando]) {
              var inserted = void 0;
              if (
                ((inserted = parent[expando]._onDragOver({
                  clientX: touchEvt.clientX,
                  clientY: touchEvt.clientY,
                  target,
                  rootEl: parent,
                })),
                inserted && !this.options.dragoverBubble)
              )
                break;
            }
            target = parent;
          } while ((parent = parent.parentNode));
        _unhideGhostForTarget();
      }
    },
    _onTouchMove: function (evt) {
      if (tapEvt) {
        var options = this.options,
          fallbackTolerance = options.fallbackTolerance,
          fallbackOffset = options.fallbackOffset,
          touch = evt.touches ? evt.touches[0] : evt,
          ghostMatrix = ghostEl && matrix(ghostEl, !0),
          scaleX = ghostEl && ghostMatrix && ghostMatrix.a,
          scaleY = ghostEl && ghostMatrix && ghostMatrix.d,
          relativeScrollOffset =
            PositionGhostAbsolutely &&
            ghostRelativeParent &&
            getRelativeScrollOffset(ghostRelativeParent),
          dx =
            (touch.clientX - tapEvt.clientX + fallbackOffset.x) / (scaleX || 1) +
            (relativeScrollOffset
              ? relativeScrollOffset[0] - ghostRelativeParentInitialScroll[0]
              : 0) /
              (scaleX || 1),
          dy =
            (touch.clientY - tapEvt.clientY + fallbackOffset.y) / (scaleY || 1) +
            (relativeScrollOffset
              ? relativeScrollOffset[1] - ghostRelativeParentInitialScroll[1]
              : 0) /
              (scaleY || 1);
        if (!Sortable.active && !awaitingDragStarted) {
          if (
            fallbackTolerance &&
            Math.max(
              Math.abs(touch.clientX - this._lastX),
              Math.abs(touch.clientY - this._lastY)
            ) < fallbackTolerance
          )
            return;
          this._onDragStart(evt, !0);
        }
        if (ghostEl) {
          ghostMatrix
            ? ((ghostMatrix.e += dx - (lastDx || 0)),
              (ghostMatrix.f += dy - (lastDy || 0)))
            : (ghostMatrix = { a: 1, b: 0, c: 0, d: 1, e: dx, f: dy });
          var cssMatrix = 'matrix('
            .concat(ghostMatrix.a, ',')
            .concat(ghostMatrix.b, ',')
            .concat(ghostMatrix.c, ',')
            .concat(ghostMatrix.d, ',')
            .concat(ghostMatrix.e, ',')
            .concat(ghostMatrix.f, ')');
          css(ghostEl, 'webkitTransform', cssMatrix),
            css(ghostEl, 'mozTransform', cssMatrix),
            css(ghostEl, 'msTransform', cssMatrix),
            css(ghostEl, 'transform', cssMatrix),
            (lastDx = dx),
            (lastDy = dy),
            (touchEvt = touch);
        }
        evt.cancelable && evt.preventDefault();
      }
    },
    _appendGhost: function () {
      if (!ghostEl) {
        var container = this.options.fallbackOnBody ? document.body : rootEl,
          rect = getRect(dragEl, !0, PositionGhostAbsolutely, !0, container),
          options = this.options;
        if (PositionGhostAbsolutely) {
          for (
            ghostRelativeParent = container;
            css(ghostRelativeParent, 'position') === 'static' &&
            css(ghostRelativeParent, 'transform') === 'none' &&
            ghostRelativeParent !== document;

          )
            ghostRelativeParent = ghostRelativeParent.parentNode;
          ghostRelativeParent !== document.body &&
          ghostRelativeParent !== document.documentElement
            ? (ghostRelativeParent === document &&
                (ghostRelativeParent = getWindowScrollingElement()),
              (rect.top += ghostRelativeParent.scrollTop),
              (rect.left += ghostRelativeParent.scrollLeft))
            : (ghostRelativeParent = getWindowScrollingElement()),
            (ghostRelativeParentInitialScroll = getRelativeScrollOffset(
              ghostRelativeParent
            ));
        }
        (ghostEl = dragEl.cloneNode(!0)),
          toggleClass(ghostEl, options.ghostClass, !1),
          toggleClass(ghostEl, options.fallbackClass, !0),
          toggleClass(ghostEl, options.dragClass, !0),
          css(ghostEl, 'transition', ''),
          css(ghostEl, 'transform', ''),
          css(ghostEl, 'box-sizing', 'border-box'),
          css(ghostEl, 'margin', 0),
          css(ghostEl, 'top', rect.top),
          css(ghostEl, 'left', rect.left),
          css(ghostEl, 'width', rect.width),
          css(ghostEl, 'height', rect.height),
          css(ghostEl, 'opacity', '0.8'),
          css(ghostEl, 'position', PositionGhostAbsolutely ? 'absolute' : 'fixed'),
          css(ghostEl, 'zIndex', '100000'),
          css(ghostEl, 'pointerEvents', 'none'),
          (Sortable.ghost = ghostEl),
          container.appendChild(ghostEl),
          css(
            ghostEl,
            'transform-origin',
            (tapDistanceLeft / parseInt(ghostEl.style.width)) * 100 +
              '% ' +
              (tapDistanceTop / parseInt(ghostEl.style.height)) * 100 +
              '%'
          );
      }
    },
    _onDragStart: function (evt, fallback) {
      var _this = this,
        dataTransfer = evt.dataTransfer,
        options = _this.options;
      if ((pluginEvent2('dragStart', this, { evt }), Sortable.eventCanceled)) {
        this._onDrop();
        return;
      }
      pluginEvent2('setupClone', this),
        Sortable.eventCanceled ||
          ((cloneEl = clone(dragEl)),
          (cloneEl.draggable = !1),
          (cloneEl.style['will-change'] = ''),
          this._hideClone(),
          toggleClass(cloneEl, this.options.chosenClass, !1),
          (Sortable.clone = cloneEl)),
        (_this.cloneId = _nextTick(function () {
          pluginEvent2('clone', _this),
            !Sortable.eventCanceled &&
              (_this.options.removeCloneOnHide || rootEl.insertBefore(cloneEl, dragEl),
              _this._hideClone(),
              _dispatchEvent({ sortable: _this, name: 'clone' }));
        })),
        !fallback && toggleClass(dragEl, options.dragClass, !0),
        fallback
          ? ((ignoreNextClick = !0),
            (_this._loopId = setInterval(_this._emulateDragOver, 50)))
          : (off(document, 'mouseup', _this._onDrop),
            off(document, 'touchend', _this._onDrop),
            off(document, 'touchcancel', _this._onDrop),
            dataTransfer &&
              ((dataTransfer.effectAllowed = 'move'),
              options.setData && options.setData.call(_this, dataTransfer, dragEl)),
            on(document, 'drop', _this),
            css(dragEl, 'transform', 'translateZ(0)')),
        (awaitingDragStarted = !0),
        (_this._dragStartId = _nextTick(_this._dragStarted.bind(_this, fallback, evt))),
        on(document, 'selectstart', _this),
        (moved = !0),
        Safari && css(document.body, 'user-select', 'none');
    },
    _onDragOver: function (evt) {
      var el = this.el,
        target = evt.target,
        dragRect,
        targetRect,
        revert,
        options = this.options,
        group = options.group,
        activeSortable = Sortable.active,
        isOwner = activeGroup === group,
        canSort = options.sort,
        fromSortable = putSortable || activeSortable,
        vertical,
        _this = this,
        completedFired = !1;
      if (_silent) return;
      function dragOverEvent(name, extra) {
        pluginEvent2(
          name,
          _this,
          _objectSpread(
            {
              evt,
              isOwner,
              axis: vertical ? 'vertical' : 'horizontal',
              revert,
              dragRect,
              targetRect,
              canSort,
              fromSortable,
              target,
              completed,
              onMove: function (target2, after2) {
                return _onMove(
                  rootEl,
                  el,
                  dragEl,
                  dragRect,
                  target2,
                  getRect(target2),
                  evt,
                  after2
                );
              },
              changed,
            },
            extra
          )
        );
      }
      function capture() {
        dragOverEvent('dragOverAnimationCapture'),
          _this.captureAnimationState(),
          _this !== fromSortable && fromSortable.captureAnimationState();
      }
      function completed(insertion) {
        return (
          dragOverEvent('dragOverCompleted', { insertion }),
          insertion &&
            (isOwner ? activeSortable._hideClone() : activeSortable._showClone(_this),
            _this !== fromSortable &&
              (toggleClass(
                dragEl,
                putSortable
                  ? putSortable.options.ghostClass
                  : activeSortable.options.ghostClass,
                !1
              ),
              toggleClass(dragEl, options.ghostClass, !0)),
            putSortable !== _this && _this !== Sortable.active
              ? (putSortable = _this)
              : _this === Sortable.active && putSortable && (putSortable = null),
            fromSortable === _this && (_this._ignoreWhileAnimating = target),
            _this.animateAll(function () {
              dragOverEvent('dragOverAnimationComplete'),
                (_this._ignoreWhileAnimating = null);
            }),
            _this !== fromSortable &&
              (fromSortable.animateAll(), (fromSortable._ignoreWhileAnimating = null))),
          ((target === dragEl && !dragEl.animated) ||
            (target === el && !target.animated)) &&
            (lastTarget = null),
          !options.dragoverBubble &&
            !evt.rootEl &&
            target !== document &&
            (dragEl.parentNode[expando]._isOutsideThisEl(evt.target),
            !insertion && nearestEmptyInsertDetectEvent(evt)),
          !options.dragoverBubble && evt.stopPropagation && evt.stopPropagation(),
          (completedFired = !0)
        );
      }
      function changed() {
        (newIndex = index(dragEl)),
          (newDraggableIndex = index(dragEl, options.draggable)),
          _dispatchEvent({
            sortable: _this,
            name: 'change',
            toEl: el,
            newIndex,
            newDraggableIndex,
            originalEvent: evt,
          });
      }
      if (
        (evt.preventDefault !== void 0 && evt.cancelable && evt.preventDefault(),
        (target = closest(target, options.draggable, el, !0)),
        dragOverEvent('dragOver'),
        Sortable.eventCanceled)
      )
        return completedFired;
      if (
        dragEl.contains(evt.target) ||
        (target.animated && target.animatingX && target.animatingY) ||
        _this._ignoreWhileAnimating === target
      )
        return completed(!1);
      if (
        ((ignoreNextClick = !1),
        activeSortable &&
          !options.disabled &&
          (isOwner
            ? canSort || (revert = !rootEl.contains(dragEl))
            : putSortable === this ||
              ((this.lastPutMode = activeGroup.checkPull(
                this,
                activeSortable,
                dragEl,
                evt
              )) &&
                group.checkPut(this, activeSortable, dragEl, evt))))
      ) {
        if (
          ((vertical = this._getDirection(evt, target) === 'vertical'),
          (dragRect = getRect(dragEl)),
          dragOverEvent('dragOverValid'),
          Sortable.eventCanceled)
        )
          return completedFired;
        if (revert)
          return (
            (parentEl = rootEl),
            capture(),
            this._hideClone(),
            dragOverEvent('revert'),
            Sortable.eventCanceled ||
              (nextEl
                ? rootEl.insertBefore(dragEl, nextEl)
                : rootEl.appendChild(dragEl)),
            completed(!0)
          );
        var elLastChild = lastChild(el, options.draggable);
        if (
          !elLastChild ||
          (_ghostIsLast(evt, vertical, this) && !elLastChild.animated)
        ) {
          if (elLastChild === dragEl) return completed(!1);
          if (
            (elLastChild && el === evt.target && (target = elLastChild),
            target && (targetRect = getRect(target)),
            _onMove(rootEl, el, dragEl, dragRect, target, targetRect, evt, !!target) !==
              !1)
          )
            return (
              capture(),
              el.appendChild(dragEl),
              (parentEl = el),
              changed(),
              completed(!0)
            );
        } else if (target.parentNode === el) {
          targetRect = getRect(target);
          var direction = 0,
            targetBeforeFirstSwap,
            differentLevel = dragEl.parentNode !== el,
            differentRowCol = !_dragElInRowColumn(
              (dragEl.animated && dragEl.toRect) || dragRect,
              (target.animated && target.toRect) || targetRect,
              vertical
            ),
            side1 = vertical ? 'top' : 'left',
            scrolledPastTop =
              isScrolledPast(target, 'top', 'top') ||
              isScrolledPast(dragEl, 'top', 'top'),
            scrollBefore = scrolledPastTop ? scrolledPastTop.scrollTop : void 0;
          lastTarget !== target &&
            ((targetBeforeFirstSwap = targetRect[side1]),
            (pastFirstInvertThresh = !1),
            (isCircumstantialInvert =
              (!differentRowCol && options.invertSwap) || differentLevel)),
            (direction = _getSwapDirection(
              evt,
              target,
              targetRect,
              vertical,
              differentRowCol ? 1 : options.swapThreshold,
              options.invertedSwapThreshold == null
                ? options.swapThreshold
                : options.invertedSwapThreshold,
              isCircumstantialInvert,
              lastTarget === target
            ));
          var sibling;
          if (direction !== 0) {
            var dragIndex = index(dragEl);
            do (dragIndex -= direction), (sibling = parentEl.children[dragIndex]);
            while (
              sibling &&
              (css(sibling, 'display') === 'none' || sibling === ghostEl)
            );
          }
          if (direction === 0 || sibling === target) return completed(!1);
          (lastTarget = target), (lastDirection = direction);
          var nextSibling = target.nextElementSibling,
            after = !1;
          after = direction === 1;
          var moveVector = _onMove(
            rootEl,
            el,
            dragEl,
            dragRect,
            target,
            targetRect,
            evt,
            after
          );
          if (moveVector !== !1)
            return (
              (moveVector === 1 || moveVector === -1) && (after = moveVector === 1),
              (_silent = !0),
              setTimeout(_unsilent, 30),
              capture(),
              after && !nextSibling
                ? el.appendChild(dragEl)
                : target.parentNode.insertBefore(dragEl, after ? nextSibling : target),
              scrolledPastTop &&
                scrollBy(scrolledPastTop, 0, scrollBefore - scrolledPastTop.scrollTop),
              (parentEl = dragEl.parentNode),
              targetBeforeFirstSwap !== void 0 &&
                !isCircumstantialInvert &&
                (targetMoveDistance = Math.abs(
                  targetBeforeFirstSwap - getRect(target)[side1]
                )),
              changed(),
              completed(!0)
            );
        }
        if (el.contains(dragEl)) return completed(!1);
      }
      return !1;
    },
    _ignoreWhileAnimating: null,
    _offMoveEvents: function () {
      off(document, 'mousemove', this._onTouchMove),
        off(document, 'touchmove', this._onTouchMove),
        off(document, 'pointermove', this._onTouchMove),
        off(document, 'dragover', nearestEmptyInsertDetectEvent),
        off(document, 'mousemove', nearestEmptyInsertDetectEvent),
        off(document, 'touchmove', nearestEmptyInsertDetectEvent);
    },
    _offUpEvents: function () {
      var ownerDocument = this.el.ownerDocument;
      off(ownerDocument, 'mouseup', this._onDrop),
        off(ownerDocument, 'touchend', this._onDrop),
        off(ownerDocument, 'pointerup', this._onDrop),
        off(ownerDocument, 'touchcancel', this._onDrop),
        off(document, 'selectstart', this);
    },
    _onDrop: function (evt) {
      var el = this.el,
        options = this.options;
      if (
        ((newIndex = index(dragEl)),
        (newDraggableIndex = index(dragEl, options.draggable)),
        pluginEvent2('drop', this, { evt }),
        (parentEl = dragEl && dragEl.parentNode),
        (newIndex = index(dragEl)),
        (newDraggableIndex = index(dragEl, options.draggable)),
        Sortable.eventCanceled)
      ) {
        this._nulling();
        return;
      }
      (awaitingDragStarted = !1),
        (isCircumstantialInvert = !1),
        (pastFirstInvertThresh = !1),
        clearInterval(this._loopId),
        clearTimeout(this._dragStartTimer),
        _cancelNextTick(this.cloneId),
        _cancelNextTick(this._dragStartId),
        this.nativeDraggable &&
          (off(document, 'drop', this), off(el, 'dragstart', this._onDragStart)),
        this._offMoveEvents(),
        this._offUpEvents(),
        Safari && css(document.body, 'user-select', ''),
        css(dragEl, 'transform', ''),
        evt &&
          (moved &&
            (evt.cancelable && evt.preventDefault(),
            !options.dropBubble && evt.stopPropagation()),
          ghostEl && ghostEl.parentNode && ghostEl.parentNode.removeChild(ghostEl),
          (rootEl === parentEl ||
            (putSortable && putSortable.lastPutMode !== 'clone')) &&
            cloneEl &&
            cloneEl.parentNode &&
            cloneEl.parentNode.removeChild(cloneEl),
          dragEl &&
            (this.nativeDraggable && off(dragEl, 'dragend', this),
            _disableDraggable(dragEl),
            (dragEl.style['will-change'] = ''),
            moved &&
              !awaitingDragStarted &&
              toggleClass(
                dragEl,
                putSortable ? putSortable.options.ghostClass : this.options.ghostClass,
                !1
              ),
            toggleClass(dragEl, this.options.chosenClass, !1),
            _dispatchEvent({
              sortable: this,
              name: 'unchoose',
              toEl: parentEl,
              newIndex: null,
              newDraggableIndex: null,
              originalEvent: evt,
            }),
            rootEl !== parentEl
              ? (newIndex >= 0 &&
                  (_dispatchEvent({
                    rootEl: parentEl,
                    name: 'add',
                    toEl: parentEl,
                    fromEl: rootEl,
                    originalEvent: evt,
                  }),
                  _dispatchEvent({
                    sortable: this,
                    name: 'remove',
                    toEl: parentEl,
                    originalEvent: evt,
                  }),
                  _dispatchEvent({
                    rootEl: parentEl,
                    name: 'sort',
                    toEl: parentEl,
                    fromEl: rootEl,
                    originalEvent: evt,
                  }),
                  _dispatchEvent({
                    sortable: this,
                    name: 'sort',
                    toEl: parentEl,
                    originalEvent: evt,
                  })),
                putSortable && putSortable.save())
              : newIndex !== oldIndex &&
                newIndex >= 0 &&
                (_dispatchEvent({
                  sortable: this,
                  name: 'update',
                  toEl: parentEl,
                  originalEvent: evt,
                }),
                _dispatchEvent({
                  sortable: this,
                  name: 'sort',
                  toEl: parentEl,
                  originalEvent: evt,
                })),
            Sortable.active &&
              ((newIndex == null || newIndex === -1) &&
                ((newIndex = oldIndex), (newDraggableIndex = oldDraggableIndex)),
              _dispatchEvent({
                sortable: this,
                name: 'end',
                toEl: parentEl,
                originalEvent: evt,
              }),
              this.save()))),
        this._nulling();
    },
    _nulling: function () {
      pluginEvent2('nulling', this),
        (rootEl = dragEl = parentEl = ghostEl = nextEl = cloneEl = lastDownEl = cloneHidden = tapEvt = touchEvt = moved = newIndex = newDraggableIndex = oldIndex = oldDraggableIndex = lastTarget = lastDirection = putSortable = activeGroup = Sortable.dragged = Sortable.ghost = Sortable.clone = Sortable.active = null),
        savedInputChecked.forEach(function (el) {
          el.checked = !0;
        }),
        (savedInputChecked.length = lastDx = lastDy = 0);
    },
    handleEvent: function (evt) {
      switch (evt.type) {
        case 'drop':
        case 'dragend':
          this._onDrop(evt);
          break;
        case 'dragenter':
        case 'dragover':
          dragEl && (this._onDragOver(evt), _globalDragOver(evt));
          break;
        case 'selectstart':
          evt.preventDefault();
          break;
      }
    },
    toArray: function () {
      for (
        var order = [],
          el,
          children = this.el.children,
          i = 0,
          n = children.length,
          options = this.options;
        i < n;
        i++
      )
        (el = children[i]),
          closest(el, options.draggable, this.el, !1) &&
            order.push(el.getAttribute(options.dataIdAttr) || _generateId(el));
      return order;
    },
    sort: function (order, useAnimation) {
      var items = {},
        rootEl2 = this.el;
      this.toArray().forEach(function (id, i) {
        var el = rootEl2.children[i];
        closest(el, this.options.draggable, rootEl2, !1) && (items[id] = el);
      }, this),
        useAnimation && this.captureAnimationState(),
        order.forEach(function (id) {
          items[id] && (rootEl2.removeChild(items[id]), rootEl2.appendChild(items[id]));
        }),
        useAnimation && this.animateAll();
    },
    save: function () {
      var store = this.options.store;
      store && store.set && store.set(this);
    },
    closest: function (el, selector) {
      return closest(el, selector || this.options.draggable, this.el, !1);
    },
    option: function (name, value) {
      var options = this.options;
      if (value === void 0) return options[name];
      var modifiedValue = PluginManager.modifyOption(this, name, value);
      typeof modifiedValue != 'undefined'
        ? (options[name] = modifiedValue)
        : (options[name] = value),
        name === 'group' && _prepareGroup(options);
    },
    destroy: function () {
      pluginEvent2('destroy', this);
      var el = this.el;
      (el[expando] = null),
        off(el, 'mousedown', this._onTapStart),
        off(el, 'touchstart', this._onTapStart),
        off(el, 'pointerdown', this._onTapStart),
        this.nativeDraggable && (off(el, 'dragover', this), off(el, 'dragenter', this)),
        Array.prototype.forEach.call(el.querySelectorAll('[draggable]'), function (
          el2
        ) {
          el2.removeAttribute('draggable');
        }),
        this._onDrop(),
        this._disableDelayedDragEvents(),
        sortables.splice(sortables.indexOf(this.el), 1),
        (this.el = el = null);
    },
    _hideClone: function () {
      if (!cloneHidden) {
        if ((pluginEvent2('hideClone', this), Sortable.eventCanceled)) return;
        css(cloneEl, 'display', 'none'),
          this.options.removeCloneOnHide &&
            cloneEl.parentNode &&
            cloneEl.parentNode.removeChild(cloneEl),
          (cloneHidden = !0);
      }
    },
    _showClone: function (putSortable2) {
      if (putSortable2.lastPutMode !== 'clone') {
        this._hideClone();
        return;
      }
      if (cloneHidden) {
        if ((pluginEvent2('showClone', this), Sortable.eventCanceled)) return;
        dragEl.parentNode == rootEl && !this.options.group.revertClone
          ? rootEl.insertBefore(cloneEl, dragEl)
          : nextEl
          ? rootEl.insertBefore(cloneEl, nextEl)
          : rootEl.appendChild(cloneEl),
          this.options.group.revertClone && this.animate(dragEl, cloneEl),
          css(cloneEl, 'display', ''),
          (cloneHidden = !1);
      }
    },
  };
  function _globalDragOver(evt) {
    evt.dataTransfer && (evt.dataTransfer.dropEffect = 'move'),
      evt.cancelable && evt.preventDefault();
  }
  function _onMove(
    fromEl,
    toEl,
    dragEl2,
    dragRect,
    targetEl,
    targetRect,
    originalEvent,
    willInsertAfter
  ) {
    var evt,
      sortable = fromEl[expando],
      onMoveFn = sortable.options.onMove,
      retVal;
    return (
      window.CustomEvent && !IE11OrLess && !Edge
        ? (evt = new CustomEvent('move', { bubbles: !0, cancelable: !0 }))
        : ((evt = document.createEvent('Event')), evt.initEvent('move', !0, !0)),
      (evt.to = toEl),
      (evt.from = fromEl),
      (evt.dragged = dragEl2),
      (evt.draggedRect = dragRect),
      (evt.related = targetEl || toEl),
      (evt.relatedRect = targetRect || getRect(toEl)),
      (evt.willInsertAfter = willInsertAfter),
      (evt.originalEvent = originalEvent),
      fromEl.dispatchEvent(evt),
      onMoveFn && (retVal = onMoveFn.call(sortable, evt, originalEvent)),
      retVal
    );
  }
  function _disableDraggable(el) {
    el.draggable = !1;
  }
  function _unsilent() {
    _silent = !1;
  }
  function _ghostIsLast(evt, vertical, sortable) {
    var rect = getRect(lastChild(sortable.el, sortable.options.draggable)),
      spacer = 10;
    return vertical
      ? evt.clientX > rect.right + spacer ||
          (evt.clientX <= rect.right &&
            evt.clientY > rect.bottom &&
            evt.clientX >= rect.left)
      : (evt.clientX > rect.right && evt.clientY > rect.top) ||
          (evt.clientX <= rect.right && evt.clientY > rect.bottom + spacer);
  }
  function _getSwapDirection(
    evt,
    target,
    targetRect,
    vertical,
    swapThreshold,
    invertedSwapThreshold,
    invertSwap,
    isLastTarget
  ) {
    var mouseOnAxis = vertical ? evt.clientY : evt.clientX,
      targetLength = vertical ? targetRect.height : targetRect.width,
      targetS1 = vertical ? targetRect.top : targetRect.left,
      targetS2 = vertical ? targetRect.bottom : targetRect.right,
      invert = !1;
    if (!invertSwap) {
      if (isLastTarget && targetMoveDistance < targetLength * swapThreshold) {
        if (
          (!pastFirstInvertThresh &&
            (lastDirection === 1
              ? mouseOnAxis > targetS1 + (targetLength * invertedSwapThreshold) / 2
              : mouseOnAxis < targetS2 - (targetLength * invertedSwapThreshold) / 2) &&
            (pastFirstInvertThresh = !0),
          pastFirstInvertThresh)
        )
          invert = !0;
        else if (
          lastDirection === 1
            ? mouseOnAxis < targetS1 + targetMoveDistance
            : mouseOnAxis > targetS2 - targetMoveDistance
        )
          return -lastDirection;
      } else if (
        mouseOnAxis > targetS1 + (targetLength * (1 - swapThreshold)) / 2 &&
        mouseOnAxis < targetS2 - (targetLength * (1 - swapThreshold)) / 2
      )
        return _getInsertDirection(target);
    }
    return (
      (invert = invert || invertSwap),
      invert &&
      (mouseOnAxis < targetS1 + (targetLength * invertedSwapThreshold) / 2 ||
        mouseOnAxis > targetS2 - (targetLength * invertedSwapThreshold) / 2)
        ? mouseOnAxis > targetS1 + targetLength / 2
          ? 1
          : -1
        : 0
    );
  }
  function _getInsertDirection(target) {
    return index(dragEl) < index(target) ? 1 : -1;
  }
  function _generateId(el) {
    for (
      var str = el.tagName + el.className + el.src + el.href + el.textContent,
        i = str.length,
        sum = 0;
      i--;

    )
      sum += str.charCodeAt(i);
    return sum.toString(36);
  }
  function _saveInputCheckedState(root) {
    savedInputChecked.length = 0;
    for (
      var inputs = root.getElementsByTagName('input'), idx = inputs.length;
      idx--;

    ) {
      var el = inputs[idx];
      el.checked && savedInputChecked.push(el);
    }
  }
  function _nextTick(fn) {
    return setTimeout(fn, 0);
  }
  function _cancelNextTick(id) {
    return clearTimeout(id);
  }
  documentExists &&
    on(document, 'touchmove', function (evt) {
      (Sortable.active || awaitingDragStarted) &&
        evt.cancelable &&
        evt.preventDefault();
    });
  Sortable.utils = {
    on,
    off,
    css,
    find,
    is: function (el, selector) {
      return !!closest(el, selector, el, !1);
    },
    extend,
    throttle,
    closest,
    toggleClass,
    clone,
    index,
    nextTick: _nextTick,
    cancelNextTick: _cancelNextTick,
    detectDirection: _detectDirection,
    getChild,
  };
  Sortable.get = function (element) {
    return element[expando];
  };
  Sortable.mount = function () {
    for (
      var _len = arguments.length, plugins2 = new Array(_len), _key = 0;
      _key < _len;
      _key++
    )
      plugins2[_key] = arguments[_key];
    plugins2[0].constructor === Array && (plugins2 = plugins2[0]),
      plugins2.forEach(function (plugin) {
        if (!plugin.prototype || !plugin.prototype.constructor)
          throw 'Sortable: Mounted plugin must be a constructor function, not '.concat(
            {}.toString.call(plugin)
          );
        plugin.utils &&
          (Sortable.utils = _objectSpread({}, Sortable.utils, plugin.utils)),
          PluginManager.mount(plugin);
      });
  };
  Sortable.create = function (el, options) {
    return new Sortable(el, options);
  };
  Sortable.version = version;
  var autoScrolls = [],
    scrollEl,
    scrollRootEl,
    scrolling = !1,
    lastAutoScrollX,
    lastAutoScrollY,
    touchEvt$1,
    pointerElemChangedInterval;
  function AutoScrollPlugin() {
    function AutoScroll() {
      this.defaults = {
        scroll: !0,
        scrollSensitivity: 30,
        scrollSpeed: 10,
        bubbleScroll: !0,
      };
      for (var fn in this)
        fn.charAt(0) === '_' &&
          typeof this[fn] == 'function' &&
          (this[fn] = this[fn].bind(this));
    }
    return (
      (AutoScroll.prototype = {
        dragStarted: function (_ref) {
          var originalEvent = _ref.originalEvent;
          this.sortable.nativeDraggable
            ? on(document, 'dragover', this._handleAutoScroll)
            : this.options.supportPointer
            ? on(document, 'pointermove', this._handleFallbackAutoScroll)
            : originalEvent.touches
            ? on(document, 'touchmove', this._handleFallbackAutoScroll)
            : on(document, 'mousemove', this._handleFallbackAutoScroll);
        },
        dragOverCompleted: function (_ref2) {
          var originalEvent = _ref2.originalEvent;
          !this.options.dragOverBubble &&
            !originalEvent.rootEl &&
            this._handleAutoScroll(originalEvent);
        },
        drop: function () {
          this.sortable.nativeDraggable
            ? off(document, 'dragover', this._handleAutoScroll)
            : (off(document, 'pointermove', this._handleFallbackAutoScroll),
              off(document, 'touchmove', this._handleFallbackAutoScroll),
              off(document, 'mousemove', this._handleFallbackAutoScroll)),
            clearPointerElemChangedInterval(),
            clearAutoScrolls(),
            cancelThrottle();
        },
        nulling: function () {
          (touchEvt$1 = scrollRootEl = scrollEl = scrolling = pointerElemChangedInterval = lastAutoScrollX = lastAutoScrollY = null),
            (autoScrolls.length = 0);
        },
        _handleFallbackAutoScroll: function (evt) {
          this._handleAutoScroll(evt, !0);
        },
        _handleAutoScroll: function (evt, fallback) {
          var _this = this,
            x = (evt.touches ? evt.touches[0] : evt).clientX,
            y = (evt.touches ? evt.touches[0] : evt).clientY,
            elem = document.elementFromPoint(x, y);
          if (((touchEvt$1 = evt), fallback || Edge || IE11OrLess || Safari)) {
            autoScroll(evt, this.options, elem, fallback);
            var ogElemScroller = getParentAutoScrollElement(elem, !0);
            scrolling &&
              (!pointerElemChangedInterval ||
                x !== lastAutoScrollX ||
                y !== lastAutoScrollY) &&
              (pointerElemChangedInterval && clearPointerElemChangedInterval(),
              (pointerElemChangedInterval = setInterval(function () {
                var newElem = getParentAutoScrollElement(
                  document.elementFromPoint(x, y),
                  !0
                );
                newElem !== ogElemScroller &&
                  ((ogElemScroller = newElem), clearAutoScrolls()),
                  autoScroll(evt, _this.options, newElem, fallback);
              }, 10)),
              (lastAutoScrollX = x),
              (lastAutoScrollY = y));
          } else {
            if (
              !this.options.bubbleScroll ||
              getParentAutoScrollElement(elem, !0) === getWindowScrollingElement()
            ) {
              clearAutoScrolls();
              return;
            }
            autoScroll(evt, this.options, getParentAutoScrollElement(elem, !1), !1);
          }
        },
      }),
      _extends(AutoScroll, { pluginName: 'scroll', initializeByDefault: !0 })
    );
  }
  function clearAutoScrolls() {
    autoScrolls.forEach(function (autoScroll2) {
      clearInterval(autoScroll2.pid);
    }),
      (autoScrolls = []);
  }
  function clearPointerElemChangedInterval() {
    clearInterval(pointerElemChangedInterval);
  }
  var autoScroll = throttle(function (evt, options, rootEl2, isFallback) {
      if (!!options.scroll) {
        var x = (evt.touches ? evt.touches[0] : evt).clientX,
          y = (evt.touches ? evt.touches[0] : evt).clientY,
          sens = options.scrollSensitivity,
          speed = options.scrollSpeed,
          winScroller = getWindowScrollingElement(),
          scrollThisInstance = !1,
          scrollCustomFn;
        scrollRootEl !== rootEl2 &&
          ((scrollRootEl = rootEl2),
          clearAutoScrolls(),
          (scrollEl = options.scroll),
          (scrollCustomFn = options.scrollFn),
          scrollEl === !0 && (scrollEl = getParentAutoScrollElement(rootEl2, !0)));
        var layersOut = 0,
          currentParent = scrollEl;
        do {
          var el = currentParent,
            rect = getRect(el),
            top = rect.top,
            bottom = rect.bottom,
            left = rect.left,
            right = rect.right,
            width = rect.width,
            height = rect.height,
            canScrollX = void 0,
            canScrollY = void 0,
            scrollWidth = el.scrollWidth,
            scrollHeight = el.scrollHeight,
            elCSS = css(el),
            scrollPosX = el.scrollLeft,
            scrollPosY = el.scrollTop;
          el === winScroller
            ? ((canScrollX =
                width < scrollWidth &&
                (elCSS.overflowX === 'auto' ||
                  elCSS.overflowX === 'scroll' ||
                  elCSS.overflowX === 'visible')),
              (canScrollY =
                height < scrollHeight &&
                (elCSS.overflowY === 'auto' ||
                  elCSS.overflowY === 'scroll' ||
                  elCSS.overflowY === 'visible')))
            : ((canScrollX =
                width < scrollWidth &&
                (elCSS.overflowX === 'auto' || elCSS.overflowX === 'scroll')),
              (canScrollY =
                height < scrollHeight &&
                (elCSS.overflowY === 'auto' || elCSS.overflowY === 'scroll')));
          var vx =
              canScrollX &&
              (Math.abs(right - x) <= sens && scrollPosX + width < scrollWidth) -
                (Math.abs(left - x) <= sens && !!scrollPosX),
            vy =
              canScrollY &&
              (Math.abs(bottom - y) <= sens && scrollPosY + height < scrollHeight) -
                (Math.abs(top - y) <= sens && !!scrollPosY);
          if (!autoScrolls[layersOut])
            for (var i = 0; i <= layersOut; i++)
              autoScrolls[i] || (autoScrolls[i] = {});
          (autoScrolls[layersOut].vx != vx ||
            autoScrolls[layersOut].vy != vy ||
            autoScrolls[layersOut].el !== el) &&
            ((autoScrolls[layersOut].el = el),
            (autoScrolls[layersOut].vx = vx),
            (autoScrolls[layersOut].vy = vy),
            clearInterval(autoScrolls[layersOut].pid),
            (vx != 0 || vy != 0) &&
              ((scrollThisInstance = !0),
              (autoScrolls[layersOut].pid = setInterval(
                function () {
                  isFallback &&
                    this.layer === 0 &&
                    Sortable.active._onTouchMove(touchEvt$1);
                  var scrollOffsetY = autoScrolls[this.layer].vy
                      ? autoScrolls[this.layer].vy * speed
                      : 0,
                    scrollOffsetX = autoScrolls[this.layer].vx
                      ? autoScrolls[this.layer].vx * speed
                      : 0;
                  (typeof scrollCustomFn == 'function' &&
                    scrollCustomFn.call(
                      Sortable.dragged.parentNode[expando],
                      scrollOffsetX,
                      scrollOffsetY,
                      evt,
                      touchEvt$1,
                      autoScrolls[this.layer].el
                    ) !== 'continue') ||
                    scrollBy(autoScrolls[this.layer].el, scrollOffsetX, scrollOffsetY);
                }.bind({ layer: layersOut }),
                24
              )))),
            layersOut++;
        } while (
          options.bubbleScroll &&
          currentParent !== winScroller &&
          (currentParent = getParentAutoScrollElement(currentParent, !1))
        );
        scrolling = scrollThisInstance;
      }
    }, 30),
    drop = function (_ref) {
      var originalEvent = _ref.originalEvent,
        putSortable2 = _ref.putSortable,
        dragEl2 = _ref.dragEl,
        activeSortable = _ref.activeSortable,
        dispatchSortableEvent = _ref.dispatchSortableEvent,
        hideGhostForTarget = _ref.hideGhostForTarget,
        unhideGhostForTarget = _ref.unhideGhostForTarget;
      if (!!originalEvent) {
        var toSortable = putSortable2 || activeSortable;
        hideGhostForTarget();
        var touch =
            originalEvent.changedTouches && originalEvent.changedTouches.length
              ? originalEvent.changedTouches[0]
              : originalEvent,
          target = document.elementFromPoint(touch.clientX, touch.clientY);
        unhideGhostForTarget(),
          toSortable &&
            !toSortable.el.contains(target) &&
            (dispatchSortableEvent('spill'),
            this.onSpill({ dragEl: dragEl2, putSortable: putSortable2 }));
      }
    };
  function Revert() {}
  Revert.prototype = {
    startIndex: null,
    dragStart: function (_ref2) {
      var oldDraggableIndex2 = _ref2.oldDraggableIndex;
      this.startIndex = oldDraggableIndex2;
    },
    onSpill: function (_ref3) {
      var dragEl2 = _ref3.dragEl,
        putSortable2 = _ref3.putSortable;
      this.sortable.captureAnimationState(),
        putSortable2 && putSortable2.captureAnimationState();
      var nextSibling = getChild(this.sortable.el, this.startIndex, this.options);
      nextSibling
        ? this.sortable.el.insertBefore(dragEl2, nextSibling)
        : this.sortable.el.appendChild(dragEl2),
        this.sortable.animateAll(),
        putSortable2 && putSortable2.animateAll();
    },
    drop,
  };
  _extends(Revert, { pluginName: 'revertOnSpill' });
  function Remove() {}
  Remove.prototype = {
    onSpill: function (_ref4) {
      var dragEl2 = _ref4.dragEl,
        putSortable2 = _ref4.putSortable,
        parentSortable = putSortable2 || this.sortable;
      parentSortable.captureAnimationState(),
        dragEl2.parentNode && dragEl2.parentNode.removeChild(dragEl2),
        parentSortable.animateAll();
    },
    drop,
  };
  _extends(Remove, { pluginName: 'removeOnSpill' });
  Sortable.mount(new AutoScrollPlugin());
  Sortable.mount(Remove, Revert);
  var sortable_esm_default = Sortable;
  var sendJSON = (url, csrfToken, data, options) => (
      (options = {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken, 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        ...options,
      }),
      data && (options.body = JSON.stringify(data)),
      fetch(url, options)
    ),
    lazyLoadImages = (elt) => {
      let lazyImages = [].slice.call(elt.querySelectorAll('img.lazy'));
      if ('IntersectionObserver' in window) {
        let lazyImageObserver = new IntersectionObserver(function (entries, observer) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              let { target } = entry;
              (target.src = target.dataset.src),
                target.classList.remove('lazy'),
                lazyImageObserver.unobserve(target);
            }
          });
        });
        lazyImages.forEach(function (img) {
          lazyImageObserver.observe(img);
        });
      } else
        lazyImages.forEach(function (img) {
          (img.src = img.dataset.src), img.classList.remove('lazy');
        });
    };
  (function () {
    window.dragDrop = (elt, options) => {
      let { csrfToken, url } = options,
        update = () => {
          let items = Array.from(elt.querySelectorAll('[data-draggable]')).map(
            (target) => target.dataset.id
          );
          items.length > 0 && sendJSON(url, csrfToken, { items });
        };
      sortable_esm_default.create(elt, {
        handle: '.handle',
        animation: 150,
        group: 'shared',
        onAdd: update,
        onRemove: update,
        onUpdate: update,
      });
    };
  })();
  var storageKey = 'player-enabled',
    defaults2 = {
      currentTime: 0,
      duration: 0,
      isPlaying: !1,
      isPaused: !1,
      isLoaded: !1,
      isStalled: !1,
      playbackRate: 1,
      counter: '00:00:00',
    },
    formatDuration = (value) => {
      if (isNaN(value) || value < 0) return '00:00:00';
      let duration = Math.floor(value),
        hours = Math.floor(duration / 3600),
        minutes = Math.floor((duration % 3600) / 60),
        seconds = Math.floor(duration % 60);
      return [hours, minutes, seconds]
        .map((t) => t.toString().padStart(2, '0'))
        .join(':');
    },
    percent = (nominator, denominator) =>
      !denominator || !nominator
        ? 0
        : denominator > nominator
        ? 100
        : (denominator / nominator) * 100;
  (function () {
    window.Player = (options) => {
      let { mediaSrc, currentTime, runImmediately, csrfToken, urls } = options || {},
        timer;
      return {
        mediaSrc,
        ...defaults2,
        initialize() {
          this.$watch('duration', (value) => {
            this.updateProgressBar(value, this.currentTime);
          }),
            this.$watch('currentTime', (value) => {
              this.updateProgressBar(this.duration, value);
            }),
            this.openPlayer();
        },
        openPlayer() {
          this.stopPlayer();
          let dataTag = document.getElementById('player-metadata');
          if (dataTag && dataTag.textContent) {
            let metadata = JSON.parse(dataTag.textContent);
            metadata &&
              'mediaSession' in navigator &&
              (Object.keys(metadata).length > 0
                ? (navigator.mediaSession.metadata = new window.MediaMetadata(metadata))
                : (navigator.mediaSession.metadata = null));
          }
          this.$nextTick(() => {
            this.$refs.audio.load();
          });
        },
        loaded() {
          !this.$refs.audio ||
            this.isLoaded ||
            ((this.$refs.audio.currentTime = currentTime),
            runImmediately || sessionStorage.getItem(storageKey)
              ? this.$refs.audio
                  .play()
                  .then(() => {
                    timer = setInterval(this.sendCurrentTimeUpdate.bind(this), 5e3);
                  })
                  .catch((e) => {
                    console.log(e), (this.isPaused = !0);
                  })
              : (this.isPaused = !0),
            (this.duration = this.$refs.audio.duration),
            (this.isLoaded = !0));
        },
        timeUpdate() {
          this.currentTime = this.$refs.audio.currentTime;
        },
        resumed() {
          (this.isPlaying = !0),
            (this.isPaused = !1),
            (this.isStalled = !1),
            sessionStorage.setItem(storageKey, !0);
        },
        paused() {
          (this.isPlaying = !1), (this.isPaused = !0), (this.isStalled = !1);
        },
        shortcuts(event) {
          if (
            !(
              /^(INPUT|SELECT|TEXTAREA)$/.test(event.target.tagName) ||
              event.ctrlKey ||
              event.altKey
            )
          ) {
            switch (event.key) {
              case '+':
                event.preventDefault(), this.incrementPlaybackRate();
                return;
              case '-':
                event.preventDefault(), this.decrementPlaybackRate();
                return;
            }
            switch (event.code) {
              case 'ArrowLeft':
                event.preventDefault(), this.skipBack();
                return;
              case 'ArrowRight':
                event.preventDefault(), this.skipForward();
                return;
              case 'Space':
                event.preventDefault(), this.togglePause();
                return;
              case 'Delete':
                event.preventDefault(), this.close();
            }
          }
        },
        incrementPlaybackRate() {
          this.changePlaybackRate(0.1);
        },
        decrementPlaybackRate() {
          this.changePlaybackRate(-0.1);
        },
        changePlaybackRate(increment) {
          let newValue = parseFloat(this.playbackRate) + increment;
          newValue > 2 ? (newValue = 2) : newValue < 0.5 && (newValue = 0.5),
            (this.$refs.audio.playbackRate = this.playbackRate = newValue);
        },
        skip({ clientX }) {
          let position = this.getProgressBarPosition(clientX);
          !isNaN(position) && position > -1 && this.skipTo(position);
        },
        skipBack() {
          this.$refs.audio && this.skipTo(this.$refs.audio.currentTime - 10);
        },
        skipForward() {
          this.$refs.audio && this.skipTo(this.$refs.audio.currentTime + 10);
        },
        skipTo(position) {
          !isNaN(position) &&
            !this.isPaused &&
            !this.isStalled &&
            (this.$refs.audio.currentTime = position);
        },
        play() {
          this.$refs.audio && this.$refs.audio.play();
        },
        pause() {
          this.$refs.audio && this.$refs.audio.pause(),
            sessionStorage.removeItem(storageKey);
        },
        error() {
          console.error('Playback Error:', this.$refs.audio.error),
            (this.isStalled = !0);
        },
        stalled() {
          console.log('Playback Stalled'), (this.isStalled = !0);
        },
        close(url) {
          this.stopPlayer(),
            window.htmx.ajax('POST', url || urls.closePlayer, { target: '#player' });
        },
        ended() {
          this.close(urls.playNextEpisode);
        },
        togglePause() {
          this.isStalled || (this.isPaused ? this.play() : this.pause());
        },
        stopPlayer() {
          this.$refs.audio && (this.$refs.audio.pause(), (this.$refs.audio = null)),
            timer && (clearInterval(timer), (timer = null));
        },
        sendCurrentTimeUpdate() {
          this.isLoaded &&
            !this.isPaused &&
            this.currentTime &&
            sendJSON(urls.timeUpdate, csrfToken, { currentTime: this.currentTime });
        },
        updateProgressBar(duration, currentTime2) {
          if (this.$refs.indicator && this.$refs.progressBar) {
            this.counter = formatDuration(duration - currentTime2);
            let pcComplete = percent(duration, currentTime2);
            this.$refs.indicator &&
              (this.$refs.indicator.style.left =
                this.getIndicatorPosition(pcComplete) + 'px');
          }
        },
        getProgressBarPosition(clientX) {
          if (isNaN(clientX)) return -1;
          {
            let { left } = this.$refs.progressBar.getBoundingClientRect(),
              width = this.$refs.progressBar.clientWidth,
              position = clientX - left;
            return Math.ceil(this.duration * (position / width));
          }
        },
        getIndicatorPosition(pcComplete) {
          let clientWidth = this.$refs.progressBar.clientWidth,
            currentPosition,
            width;
          if (
            ((currentPosition =
              this.$refs.progressBar.getBoundingClientRect().left - 24),
            clientWidth === 0)
          )
            width = 0;
          else {
            let minWidth = (16 / clientWidth) * 100;
            width = pcComplete > minWidth ? pcComplete : minWidth;
          }
          return (
            width && (currentPosition += clientWidth * (width / 100)), currentPosition
          );
        },
      };
    };
  })();
  document.addEventListener('htmx:afterSwap', (event) => {
    event.target.id === 'content' && window.scrollTo(0, event.target.offsetTop - 160);
  });
  document.addEventListener('htmx:load', (event) => lazyLoadImages(event.detail.elt));
  document.addEventListener('DOMContentLoaded', lazyLoadImages(document));
})();
/**!
 * Sortable 1.13.0
 * @author	RubaXa   <trash@rubaxa.org>
 * @author	owenm    <owen23355@gmail.com>
 * @license MIT
 */
