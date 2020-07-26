在阅读hadoop相关源码的过程中，经常见到类似  

```
@InterfaceAudience.Public
@InterfaceStability.Stable
```  
之类的标识。特意查阅了一下相关资料，在此做一个小结  

## 1.InterfaceAudience 
InterfaceAudience 类包含有三个注解类型，用来说明被他们注解的类型的潜在使用范围，即audience  

InterfaceAudience的源码如下  
```
/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.hadoop.classification;

import java.lang.annotation.Documented;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

/**
 * Annotation to inform users of a package, class or method's intended audience.
 */
@InterfaceAudience.Public
@InterfaceStability.Evolving
public class InterfaceAudience {
  /**
   * Intended for use by any project or application.
   */
  @Documented
  @Retention(RetentionPolicy.RUNTIME)
  public @interface Public {};
  
  /**
   * Intended only for the project(s) specified in the annotation.
   * For example, "Common", "HDFS", "MapReduce", "ZooKeeper", "HBase".
   */
  @Documented
  @Retention(RetentionPolicy.RUNTIME)
  public @interface LimitedPrivate {
    String[] value();
  };
  
  /**
   * Intended for use only within Hadoop itself.
   */
  @Documented
  @Retention(RetentionPolicy.RUNTIME)
  public @interface Private {};

  private InterfaceAudience() {} // Audience can't exist on its own
}

```   

从源码中很容易看出来：  
1.如果标注的是Public，说明被注解的类型对多有工程和应用可用。  
2.如果标注的是LimitedPrivate,说明被注解的类型只能用于某些特定的工程或应用，如Common,HDFS,MapReduce,ZooKeeper,HBase等。  
3.如果标注的是Private，说明被注解的类型只能用于Hadoop。  

## 2.InterfaceStability
InterfaceStability 类包含三个注解，用于说明被他们注解的类型的稳定性。  
InterfaceStability源码如下  

```
/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.hadoop.classification;

import java.lang.annotation.Documented;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

/**
 * Annotation to inform users of how much to rely on a particular package,
 * class or method not changing over time.
 * </ul>
 */
@InterfaceAudience.Public
@InterfaceStability.Evolving
public class InterfaceStability {
  /**
   * Can evolve while retaining compatibility for minor release boundaries.; 
   * can break compatibility only at major release (ie. at m.0).
   */
  @Documented
  @Retention(RetentionPolicy.RUNTIME)
  public @interface Stable {};
  
  /**
   * Evolving, but can break compatibility at minor release (i.e. m.x)
   */
  @Documented
  @Retention(RetentionPolicy.RUNTIME)
  public @interface Evolving {};
  
  /**
   * No guarantee is provided as to reliability or stability across any
   * level of release granularity.
   */
  @Documented
  @Retention(RetentionPolicy.RUNTIME)
  public @interface Unstable {};
}

```  

从上述源码也很容易看出：  
1.如果标注的是Stable，说明主版本是稳定的，不同主版本之间可能不兼容。  
2.如果标注的是Evolving，说明是不停在变化的，不同小版本之间也可能不兼容。    
3.如果标注的是Unstable，说明稳定性没有任何保证。  