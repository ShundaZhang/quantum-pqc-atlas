import test from 'node:test';
import assert from 'node:assert/strict';
import {groverState,shorSample} from '../algorithm-labs.mjs';
const close=(actual,expected,tolerance=1e-11)=>assert.ok(Math.abs(actual-expected)<tolerance,`${actual} != ${expected}`);
test('four-item example reaches its unique target after one complete iteration',()=>{
  assert.deepEqual(groverState(4,0).amplitudes,[0.5,0.5,0.5,0.5]);
  assert.deepEqual(groverState(4,0,true).amplitudes,[-0.5,0.5,0.5,0.5]);
  assert.deepEqual(groverState(4,1).amplitudes,[1,0,0,0]);
});
test('iterated vectors remain normalized and agree with the independent rotation formula',()=>{
  for(const N of [4,16,64])for(let k=0;k<=12;k++){
    const state=groverState(N,k);
    close(state.probabilities.reduce((a,b)=>a+b,0),1);
    close(state.probabilities[0],Math.sin((2*k+1)*Math.asin(1/Math.sqrt(N)))**2);
    assert.deepEqual(groverState(N,k,true).probabilities,state.probabilities);
  }
});
test('overshooting the first peak reduces success',()=>{
  assert.ok(groverState(16,3).probabilities[0]>groverState(16,4).probabilities[0]);
  assert.ok(groverState(64,6).probabilities[0]>groverState(64,7).probabilities[0]);
});
test('Shor postprocessing distinguishes good, reduced and uninformative phase samples',()=>{
  for(const c of [64,192]){
    const sample=shorSample(c);
    assert.equal(sample.status,'factors');assert.equal(sample.denominator,4);
    assert.deepEqual(sample.factors,[3,5]);assert.equal(sample.factors.reduce((a,b)=>a*b),15);
  }
  assert.equal(shorSample(128).denominator,2);assert.equal(shorSample(128).status,'retry');
  assert.deepEqual(shorSample(128).factors,[]);
  assert.equal(shorSample(0).status,'uninformative');assert.deepEqual(shorSample(0).factors,[]);
});
test('models reject unsupported inputs rather than implying general factoring or search',()=>{
  for(const args of [[3,1],[4,-1],[4,13],[16,1.5]])assert.throws(()=>groverState(...args),RangeError);
  assert.throws(()=>shorSample(63),RangeError);
});
